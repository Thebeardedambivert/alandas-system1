"""Safe, configurable provider adapters and dry-run planner for Firecrawl & Apify.

Zero live network calls by default. Designed for test/staging safety now and
production waterfall evolution later.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
import ipaddress
import json
import os
import re
import socket
import sys
from typing import Any, Callable, Mapping, Sequence
from urllib.error import HTTPError
from urllib.parse import urlparse

from system_1 import db
from system_1.provider_http import HttpResponse, HttpTransport, UrllibHttpTransport


# ---------------------------------------------------------------------------
# Actor ID Normalization & Validation
# ---------------------------------------------------------------------------

_ACTOR_PART_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")
_ACTOR_NAME_REGEX = re.compile(r"^[a-zA-Z0-9._-]+$")


def normalize_and_validate_actor_id(raw_actor: str) -> str:
    """Normalize store-style 'owner/actor' to REST-safe 'owner~actor' and validate.

    Fails closed on empty, malformed, or invalid actor IDs.
    """
    actor = raw_actor.strip()
    if not actor:
        raise ValueError("Actor ID cannot be empty")
    if len(actor) > 100:
        raise ValueError(f"Actor ID '{actor}' is excessively long (>100 characters)")

    if "/" in actor:
        parts = actor.split("/")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(f"Invalid store-style actor ID: '{raw_actor}'")
        owner, name = parts[0], parts[1]
    elif "~" in actor:
        parts = actor.split("~")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(f"Invalid REST-style actor ID: '{raw_actor}'")
        owner, name = parts[0], parts[1]
    else:
        # Legacy/standalone single identifier without owner prefix
        if not _ACTOR_PART_REGEX.match(actor):
            raise ValueError(f"Invalid actor ID: '{raw_actor}'")
        return actor

    if not _ACTOR_PART_REGEX.match(owner) or not _ACTOR_NAME_REGEX.match(name):
        raise ValueError(f"Invalid characters in actor ID: '{raw_actor}'")

    return f"{owner}~{name}"


# ---------------------------------------------------------------------------
# URL Validation & Security Rejection (SSRF Protection)
# ---------------------------------------------------------------------------

def validate_scrape_target_url(
    value: str,
    resolver: Callable[..., list[tuple[object, object, object, object, tuple[str, int]]]] = socket.getaddrinfo,
) -> str:
    """Validate that target URL is a public http/https destination.

    Rejects non-web schemes, credentials, non-standard ports, localhost,
    and private/internal/RFC1918 networks.
    """
    url_str = value.strip()
    if not url_str:
        raise ValueError("Target URL cannot be empty")

    parsed = urlparse(url_str)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Target URL must use http or https scheme")
    if not parsed.hostname:
        raise ValueError("Target URL must have a valid hostname")
    if parsed.username or parsed.password:
        raise ValueError("Target URL cannot contain credentials")
    if parsed.port not in {None, 80, 443}:
        raise ValueError("Target URL may use only standard web ports (80 or 443)")

    host_lower = parsed.hostname.lower()
    if host_lower in {"localhost"} or host_lower.endswith(".local") or host_lower.endswith(".internal"):
        raise ValueError(f"Private/internal target host '{parsed.hostname}' is rejected")

    # Check if host is already a numeric IP literal
    try:
        ip = ipaddress.ip_address(host_lower)
        if not ip.is_global:
            raise ValueError(f"Non-public target IP '{parsed.hostname}' is rejected")
        return parsed.geturl()
    except ValueError as err:
        if "rejected" in str(err):
            raise

    # Resolve hostname to verify IP is global/public
    try:
        addresses = resolver(parsed.hostname, None, type=socket.SOCK_STREAM)
    except OSError as error:
        raise ValueError(f"Could not resolve target host: {parsed.hostname}") from error

    if not addresses:
        raise ValueError("Target host resolved to no addresses")

    for address in addresses:
        resolved_ip = ipaddress.ip_address(address[4][0])
        if not resolved_ip.is_global:
            raise ValueError(f"Target host resolved to a non-public address: {resolved_ip}")

    return parsed.geturl()


# ---------------------------------------------------------------------------
# Outcome Types & Status Codes
# ---------------------------------------------------------------------------

class EnrichmentStatus(str, Enum):
    SUCCESS = "success"
    NO_RESULT_FOUND = "no_result_found"
    PROVIDER_DISABLED = "provider_disabled"
    MISSING_CREDENTIALS = "missing_credentials"
    INVALID_ACTOR_ID = "invalid_actor_id"
    INVALID_URL = "invalid_url"
    PRIVATE_URL_REJECTED = "private_url_rejected"
    MISSING_RESULT_CAP = "missing_result_cap"
    RESULT_CAP_EXCEEDED = "result_cap_exceeded"
    COST_CAP_EXCEEDED = "cost_cap_exceeded"
    PROVIDER_TIMEOUT = "provider_timeout"
    PROVIDER_AUTH_FAILED = "provider_auth_failed"
    PROVIDER_REJECTED = "provider_rejected"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    PROVIDER_MALFORMED_RESPONSE = "provider_malformed_response"
    AMBIGUOUS_SOCIAL_MATCH = "ambiguous_social_match"
    SCHEMA_MISMATCH = "schema_mismatch"
    NEEDS_RECONCILIATION = "needs_reconciliation"
    BLOCKED_BY_DEFAULT = "blocked_by_default"


@dataclass(frozen=True)
class ProviderExecutionResult:
    """Structured, auditable provider outcome surfaced to operators."""

    provider: str
    status: str
    data: dict[str, Any] = field(default_factory=dict)
    operator_message: str = ""
    next_action: str = ""
    run_id: str = ""


def extract_provider_error_message(body: Any) -> str:
    """Safely extract error message from response body, redacting potential secrets."""
    if not body:
        return ""
    if isinstance(body, str):
        msg = body
    elif isinstance(body, dict):
        err = body.get("error")
        msg = ""
        if isinstance(err, str):
            msg = err
        elif isinstance(err, dict):
            msg = str(err.get("message") or err.get("description") or err.get("detail") or "")
        if not msg:
            msg = str(body.get("message") or body.get("description") or body.get("detail") or "")
    else:
        msg = str(body)

    # Redact any tokens, credentials, or secrets that might appear in error strings
    sanitized = re.sub(
        r"(?i)(api[_-]?key|token|bearer|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-\.]+['\"]?",
        r"\1=[REDACTED]",
        msg,
    )
    sanitized = re.sub(r"fc-[A-Za-z0-9_\-]+", "[REDACTED_KEY]", sanitized)
    sanitized = re.sub(r"apify_api_[A-Za-z0-9_\-]+", "[REDACTED_KEY]", sanitized)
    return sanitized.strip()


def map_provider_http_response(
    provider: str,
    response: HttpResponse,
    expected_schema_keys: Sequence[str] = (),
) -> ProviderExecutionResult:
    """Map raw HTTP response to structured production outcome."""
    status_code = response.status_code
    body = response.json_body

    if status_code in (401, 403):
        detail = extract_provider_error_message(body)
        detail_suffix = f": {detail}" if detail else ""
        return ProviderExecutionResult(
            provider=provider,
            status=EnrichmentStatus.PROVIDER_AUTH_FAILED.value,
            data=body if isinstance(body, (dict, list)) else {},
            operator_message=f"{provider} authentication failed (HTTP {status_code}){detail_suffix}. Verify API token/key.",
            next_action="operator_check_credentials",
        )
    if 400 <= status_code < 500:
        detail = extract_provider_error_message(body)
        detail_suffix = f": {detail}" if detail else ". Inspect payload and parameters."
        return ProviderExecutionResult(
            provider=provider,
            status=EnrichmentStatus.PROVIDER_REJECTED.value,
            data=body if isinstance(body, (dict, list)) else {},
            operator_message=f"{provider} rejected request (HTTP {status_code}){detail_suffix}",
            next_action="operator_review_payload",
        )
    if status_code >= 500:
        detail = extract_provider_error_message(body)
        detail_suffix = f": {detail}" if detail else ""
        return ProviderExecutionResult(
            provider=provider,
            status=EnrichmentStatus.PROVIDER_UNAVAILABLE.value,
            data=body if isinstance(body, (dict, list)) else {},
            operator_message=f"{provider} service unavailable (HTTP {status_code}){detail_suffix}. Defer run until service recovery.",
            next_action="defer_and_retry_later",
        )
    if status_code not in (200, 201):
        return ProviderExecutionResult(
            provider=provider,
            status=EnrichmentStatus.NEEDS_RECONCILIATION.value,
            operator_message=f"{provider} returned unexpected HTTP status {status_code}.",
            next_action="needs_reconciliation",
        )

    # Validate JSON payload structure
    if not isinstance(body, (dict, list)):
        return ProviderExecutionResult(
            provider=provider,
            status=EnrichmentStatus.PROVIDER_MALFORMED_RESPONSE.value,
            operator_message=f"{provider} returned malformed or non-JSON body.",
            next_action="operator_inspect_response",
        )

    # Empty result handling: not treated as a failure/crash
    if not body:
        return ProviderExecutionResult(
            provider=provider,
            status=EnrichmentStatus.NO_RESULT_FOUND.value,
            operator_message=f"{provider} returned empty response body.",
            next_action="proceed_with_available_evidence",
        )
    if isinstance(body, dict):
        inner_items = body.get("data") if "data" in body else body.get("items")
        if isinstance(inner_items, (list, dict)) and len(inner_items) == 0:
            return ProviderExecutionResult(
                provider=provider,
                status=EnrichmentStatus.NO_RESULT_FOUND.value,
                data=body,
                operator_message=f"{provider} executed successfully but found 0 matching items.",
                next_action="proceed_with_available_evidence",
            )

    # Schema validation
    if expected_schema_keys and isinstance(body, dict):
        missing = [k for k in expected_schema_keys if k not in body]
        if missing:
            return ProviderExecutionResult(
                provider=provider,
                status=EnrichmentStatus.SCHEMA_MISMATCH.value,
                data=body,
                operator_message=f"{provider} response schema changed; missing expected keys: {', '.join(missing)}.",
                next_action="block_automation_and_update_schema",
            )

    run_id = ""
    if isinstance(body, dict):
        inner_data = body.get("data")
        if isinstance(inner_data, dict):
            run_id = str(inner_data.get("id") or "")
        elif isinstance(inner_data, list) and inner_data and isinstance(inner_data[0], dict):
            run_id = str(inner_data[0].get("id") or "")
        if not run_id:
            run_id = str(body.get("id") or "")

    return ProviderExecutionResult(
        provider=provider,
        status=EnrichmentStatus.SUCCESS.value,
        data=body if isinstance(body, dict) else {"items": body},
        operator_message=f"{provider} completed successfully.",
        next_action="proceed_to_next_step",
        run_id=run_id,
    )


# ---------------------------------------------------------------------------
# Ambiguity & Fallback Evaluation
# ---------------------------------------------------------------------------

def check_social_match_ambiguity(
    target_handle_or_url: str,
    results: list[dict[str, Any]],
) -> tuple[bool, str]:
    """Check if social scrape results contain ambiguity or handle mismatches."""
    if len(results) > 1:
        return True, f"Multiple profiles ({len(results)}) returned for query; requires operator review"
    if not results:
        return False, "no_results"

    first = results[0]
    returned_user = str(first.get("username") or first.get("handle") or "").strip().lower()
    expected_user = target_handle_or_url.split("/")[-1].replace("@", "").strip().lower()
    if returned_user and expected_user and returned_user != expected_user:
        return True, f"Returned username '{returned_user}' does not match target '{expected_user}'; requires operator review"
    return False, "ok"


@dataclass(frozen=True)
class WaterfallStepOutcome:
    step_name: str
    status: str
    operator_action: str
    notes: str


def evaluate_waterfall_fallbacks(
    firecrawl_outcome: ProviderExecutionResult | None,
    instagram_outcome: ProviderExecutionResult | None,
    facebook_outcome: ProviderExecutionResult | None,
) -> dict[str, WaterfallStepOutcome]:
    """Apply fallback design rules across waterfall steps.

    - Firecrawl scrape fails -> no automatic paid fallback; mark website_review_needs_operator_review.
    - Instagram actor fails -> keep lead usable with Firecrawl/Facebook results; mark instagram_review_failed.
    - Facebook actor fails -> keep lead usable with Firecrawl/Instagram results; mark facebook_review_failed.
    """
    outcomes: dict[str, WaterfallStepOutcome] = {}

    if firecrawl_outcome is not None:
        if firecrawl_outcome.status == EnrichmentStatus.SUCCESS.value:
            outcomes["website_review"] = WaterfallStepOutcome(
                step_name="website_review",
                status="completed",
                operator_action="proceed",
                notes="Website scrape succeeded",
            )
        elif firecrawl_outcome.status == EnrichmentStatus.NO_RESULT_FOUND.value:
            outcomes["website_review"] = WaterfallStepOutcome(
                step_name="website_review",
                status="no_result_found",
                operator_action="website_review_needs_operator_review",
                notes="No content found at website URL",
            )
        else:
            outcomes["website_review"] = WaterfallStepOutcome(
                step_name="website_review",
                status="failed",
                operator_action="website_review_needs_operator_review",
                notes=f"Firecrawl failed ({firecrawl_outcome.status}): {firecrawl_outcome.operator_message}",
            )

    if instagram_outcome is not None:
        if instagram_outcome.status == EnrichmentStatus.SUCCESS.value:
            outcomes["instagram_review"] = WaterfallStepOutcome(
                step_name="instagram_review",
                status="completed",
                operator_action="proceed",
                notes="Instagram scrape succeeded",
            )
        elif instagram_outcome.status == EnrichmentStatus.AMBIGUOUS_SOCIAL_MATCH.value:
            outcomes["instagram_review"] = WaterfallStepOutcome(
                step_name="instagram_review",
                status="ambiguous_social_match",
                operator_action="operator_review_needed",
                notes=instagram_outcome.operator_message,
            )
        else:
            outcomes["instagram_review"] = WaterfallStepOutcome(
                step_name="instagram_review",
                status="instagram_review_failed",
                operator_action="operator_review_needed",
                notes=f"Instagram actor failed ({instagram_outcome.status}): {instagram_outcome.operator_message}",
            )

    if facebook_outcome is not None:
        if facebook_outcome.status == EnrichmentStatus.SUCCESS.value:
            outcomes["facebook_review"] = WaterfallStepOutcome(
                step_name="facebook_review",
                status="completed",
                operator_action="proceed",
                notes="Facebook scrape succeeded",
            )
        elif facebook_outcome.status == EnrichmentStatus.AMBIGUOUS_SOCIAL_MATCH.value:
            outcomes["facebook_review"] = WaterfallStepOutcome(
                step_name="facebook_review",
                status="ambiguous_social_match",
                operator_action="operator_review_needed",
                notes=facebook_outcome.operator_message,
            )
        else:
            outcomes["facebook_review"] = WaterfallStepOutcome(
                step_name="facebook_review",
                status="facebook_review_failed",
                operator_action="operator_review_needed",
                notes=f"Facebook actor failed ({facebook_outcome.status}): {facebook_outcome.operator_message}",
            )

    return outcomes


# ---------------------------------------------------------------------------
# Provider Configurations & Safety Guards
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FirecrawlConfig:
    api_key: str
    enabled: bool = False
    mode: str = "staging"
    max_credits_per_run: int = 10
    max_pages_per_lead: int = 2
    api_url: str = "https://api.firecrawl.dev/v1/scrape"
    formats: tuple[str, ...] = ("markdown",)
    only_main_content: bool = True

    @classmethod
    def from_env(cls) -> "FirecrawlConfig":
        mode = os.environ.get("SYSTEM1_ENRICHMENT_MODE", "staging").strip().lower()
        if mode not in {"staging", "production"}:
            mode = "staging"

        enabled = os.environ.get("SYSTEM1_FIRECRAWL_ENABLED", "").lower() in {"1", "true", "yes"}
        api_key = os.environ.get("FIRECRAWL_API_KEY", "")

        default_credits = "10" if mode == "staging" else "50"
        default_pages = "2" if mode == "staging" else "5"
        raw_credits = os.environ.get("SYSTEM1_FIRECRAWL_MAX_CREDITS_PER_RUN", default_credits)
        raw_pages = os.environ.get("SYSTEM1_FIRECRAWL_MAX_PAGES_PER_LEAD", default_pages)
        api_url = (
            os.environ.get("SYSTEM1_FIRECRAWL_API_URL", "https://api.firecrawl.dev/v1/scrape").strip()
            or "https://api.firecrawl.dev/v1/scrape"
        )

        max_credits = int(raw_credits)
        max_pages = int(raw_pages)
        if max_credits <= 0:
            raise ValueError("Firecrawl max credits per run must be positive")
        if max_pages <= 0:
            raise ValueError("Firecrawl max pages per lead must be positive")

        return cls(
            api_key=api_key,
            enabled=enabled,
            mode=mode,
            max_credits_per_run=max_credits,
            max_pages_per_lead=max_pages,
            api_url=api_url,
        )


@dataclass(frozen=True)
class ApifyEnrichmentConfig:
    api_token: str
    enabled: bool = False
    mode: str = "staging"
    max_cost_usd: Decimal = Decimal("0.50")
    max_results_per_actor: int = 5
    instagram_profile_actors: tuple[str, ...] = ()
    facebook_page_actors: tuple[str, ...] = ()
    people_fallback_actors: tuple[str, ...] = ()

    @classmethod
    def from_env(cls) -> "ApifyEnrichmentConfig":
        mode = os.environ.get("SYSTEM1_ENRICHMENT_MODE", "staging").strip().lower()
        if mode not in {"staging", "production"}:
            mode = "staging"

        enabled = os.environ.get("SYSTEM1_APIFY_ENRICHMENT_ENABLED", "").lower() in {"1", "true", "yes"}
        token = os.environ.get("APIFY_API_TOKEN", "")

        default_cost = "0.50" if mode == "staging" else "1.00"
        default_results = "5" if mode == "staging" else "10"
        raw_cost = os.environ.get("SYSTEM1_APIFY_ENRICHMENT_MAX_COST_USD", default_cost)
        raw_results = os.environ.get("SYSTEM1_APIFY_ENRICHMENT_MAX_RESULTS_PER_ACTOR", default_results)

        max_cost = Decimal(raw_cost)
        max_results = int(raw_results)
        if max_cost <= Decimal("0.00"):
            raise ValueError("Apify enrichment max cost must be positive")
        if max_results <= 0:
            raise ValueError("Apify enrichment max results must be positive")

        def parse_actors(env_var: str) -> tuple[str, ...]:
            raw = os.environ.get(env_var, "").strip()
            if not raw:
                return ()
            actors = []
            for item in raw.split(","):
                item_str = item.strip()
                if item_str:
                    actors.append(normalize_and_validate_actor_id(item_str))
            return tuple(actors)

        return cls(
            api_token=token,
            enabled=enabled,
            mode=mode,
            max_cost_usd=max_cost,
            max_results_per_actor=max_results,
            instagram_profile_actors=parse_actors("SYSTEM1_APIFY_INSTAGRAM_PROFILE_ACTORS"),
            facebook_page_actors=parse_actors("SYSTEM1_APIFY_FACEBOOK_PAGE_ACTORS"),
            people_fallback_actors=parse_actors("SYSTEM1_APIFY_PEOPLE_FALLBACK_ACTORS"),
        )


# ---------------------------------------------------------------------------
# Provider Adapters (Safe, Bounded, Production-Shaped)
# ---------------------------------------------------------------------------

class FirecrawlAdapter:
    """Safe adapter for Firecrawl web scraping.

    Enforces disabled switch, public URL verification, credit caps, and safe JSON serialization.
    """

    def __init__(self, config: FirecrawlConfig, transport: HttpTransport | None = None) -> None:
        self.config = config
        self._transport = transport or UrllibHttpTransport()

    def scrape_url(
        self,
        target_url: str,
        pages_limit: int | None = None,
        resolver: Callable[..., list[tuple]] = socket.getaddrinfo,
    ) -> ProviderExecutionResult:
        if not self.config.enabled:
            return ProviderExecutionResult(
                provider="firecrawl",
                status=EnrichmentStatus.PROVIDER_DISABLED.value,
                operator_message="Firecrawl enrichment is disabled (SYSTEM1_FIRECRAWL_ENABLED=false).",
                next_action="none_skipped",
            )
        if not self.config.api_key:
            return ProviderExecutionResult(
                provider="firecrawl",
                status=EnrichmentStatus.MISSING_CREDENTIALS.value,
                operator_message="FIRECRAWL_API_KEY is missing from environment.",
                next_action="operator_configure_key",
            )

        try:
            validated_url = validate_scrape_target_url(target_url, resolver=resolver)
        except ValueError as err:
            err_msg = str(err)
            status = (
                EnrichmentStatus.PRIVATE_URL_REJECTED.value
                if "non-public" in err_msg or "Private/internal" in err_msg
                else EnrichmentStatus.INVALID_URL.value
            )
            return ProviderExecutionResult(
                provider="firecrawl",
                status=status,
                operator_message=err_msg,
                next_action="operator_review_url",
            )

        limit = pages_limit or self.config.max_pages_per_lead
        if limit <= 0:
            return ProviderExecutionResult(
                provider="firecrawl",
                status=EnrichmentStatus.MISSING_RESULT_CAP.value,
                operator_message="Firecrawl pages limit must be positive.",
                next_action="operator_review_config",
            )
        if limit > self.config.max_pages_per_lead:
            return ProviderExecutionResult(
                provider="firecrawl",
                status=EnrichmentStatus.RESULT_CAP_EXCEEDED.value,
                operator_message=f"Requested pages ({limit}) exceeds configured max pages ({self.config.max_pages_per_lead}).",
                next_action="operator_review_config",
            )

        # Enforce Firecrawl credit cap before any network call (1 credit per page)
        estimated_credits = limit
        if self.config.max_credits_per_run <= 0 or estimated_credits > self.config.max_credits_per_run:
            return ProviderExecutionResult(
                provider="firecrawl",
                status=EnrichmentStatus.COST_CAP_EXCEEDED.value,
                operator_message=(
                    f"Estimated scrape credits ({estimated_credits}) exceeds configured max credits "
                    f"({self.config.max_credits_per_run})."
                ),
                next_action="operator_review_config",
            )

        payload = json.dumps(
            {
                "url": validated_url,
                "formats": list(self.config.formats),
                "onlyMainContent": self.config.only_main_content,
            },
            ensure_ascii=True,
        ).encode("utf-8")

        try:
            resp = self._transport.request(
                method="POST",
                url=self.config.api_url,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                },
                body=payload,
                timeout_seconds=30,
            )
        except (TimeoutError, socket.timeout):
            return ProviderExecutionResult(
                provider="firecrawl",
                status=EnrichmentStatus.PROVIDER_TIMEOUT.value,
                operator_message="Firecrawl request timed out after 30s. Do not retry blindly.",
                next_action="inspect_firecrawl_status",
            )
        except HTTPError as error:
            try:
                err_payload = error.read()
            finally:
                error.close()
            decoded = None
            if err_payload:
                try:
                    decoded = json.loads(err_payload.decode("utf-8"))
                except Exception:
                    decoded = {"error": err_payload.decode("utf-8", errors="replace")}
            resp = HttpResponse(error.code, decoded if decoded is not None else {})
            return map_provider_http_response("firecrawl", resp)
        except Exception as error:
            return ProviderExecutionResult(
                provider="firecrawl",
                status=EnrichmentStatus.PROVIDER_UNAVAILABLE.value,
                operator_message=f"Firecrawl transport failure: {error}",
                next_action="inspect_firecrawl_status",
            )

        return map_provider_http_response("firecrawl", resp)


class ApifyEnrichmentAdapter:
    """Safe adapter for Apify social and people enrichment actors."""

    def __init__(self, config: ApifyEnrichmentConfig, transport: HttpTransport | None = None) -> None:
        self.config = config
        self._transport = transport or UrllibHttpTransport()

    def run_actor(
        self,
        actor_id: str,
        group: str,
        input_data: dict[str, Any],
        estimated_cost_usd: Decimal,
        max_results: int | None = None,
        approved_by: str | None = None,
    ) -> ProviderExecutionResult:
        provider_name = f"apify_{group}"

        if not self.config.enabled:
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.PROVIDER_DISABLED.value,
                operator_message="Apify enrichment is disabled (SYSTEM1_APIFY_ENRICHMENT_ENABLED=false).",
                next_action="none_skipped",
            )
        if not self.config.api_token:
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.MISSING_CREDENTIALS.value,
                operator_message="APIFY_API_TOKEN is missing from environment.",
                next_action="operator_configure_key",
            )

        try:
            normalized_actor = normalize_and_validate_actor_id(actor_id)
        except ValueError as err:
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.INVALID_ACTOR_ID.value,
                operator_message=str(err),
                next_action="operator_fix_actor_id",
            )

        effective_max_results = self.config.max_results_per_actor if max_results is None else max_results
        if effective_max_results <= 0:
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.MISSING_RESULT_CAP.value,
                operator_message="Apify max results cap must be positive.",
                next_action="operator_review_config",
            )
        if effective_max_results > self.config.max_results_per_actor:
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.RESULT_CAP_EXCEEDED.value,
                operator_message=f"Requested results ({effective_max_results}) exceeds configured max ({self.config.max_results_per_actor}).",
                next_action="operator_review_config",
            )

        if estimated_cost_usd <= Decimal("0.00"):
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.COST_CAP_EXCEEDED.value,
                operator_message="Estimated cost must be positive.",
                next_action="operator_review_cost",
            )
        if estimated_cost_usd > self.config.max_cost_usd:
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.COST_CAP_EXCEEDED.value,
                operator_message=f"Estimated cost (${estimated_cost_usd:.2f}) exceeds configured max cost (${self.config.max_cost_usd:.2f}).",
                next_action="operator_review_cost",
            )

        if group == "people_fallback" and not approved_by:
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.BLOCKED_BY_DEFAULT.value,
                operator_message="People/email/phone fallback actors are blocked by default; explicit approval is required.",
                next_action="wait_for_human_approval",
            )

        payload = json.dumps(input_data, ensure_ascii=True).encode("utf-8")
        url = (
            f"https://api.apify.com/v2/acts/{normalized_actor}/runs"
            f"?maxTotalChargeUsd={estimated_cost_usd:.2f}&maxItems={effective_max_results}"
        )

        try:
            resp = self._transport.request(
                method="POST",
                url=url,
                headers={
                    "Authorization": f"Bearer {self.config.api_token}",
                    "Content-Type": "application/json",
                },
                body=payload,
                timeout_seconds=30,
            )
        except (TimeoutError, socket.timeout):
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.PROVIDER_TIMEOUT.value,
                operator_message=f"Apify request to actor '{normalized_actor}' timed out. Do not retry blindly.",
                next_action="reconcile_apify_run",
            )
        except HTTPError as error:
            try:
                err_payload = error.read()
            finally:
                error.close()
            decoded = None
            if err_payload:
                try:
                    decoded = json.loads(err_payload.decode("utf-8"))
                except Exception:
                    decoded = {"error": err_payload.decode("utf-8", errors="replace")}
            resp = HttpResponse(error.code, decoded if decoded is not None else {})
            return map_provider_http_response(provider_name, resp)
        except Exception as error:
            return ProviderExecutionResult(
                provider=provider_name,
                status=EnrichmentStatus.PROVIDER_UNAVAILABLE.value,
                operator_message=f"Apify transport failure: {error}",
                next_action="reconcile_apify_run",
            )

        return map_provider_http_response(provider_name, resp)


# ---------------------------------------------------------------------------
# Dry-Run Enrichment Routing Logic
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PlannedEnrichmentAction:
    provider: str
    target_type: str
    target_value: str
    actor_id: str = ""
    status: str = "would_route"
    reason: str = ""


def plan_lead_provider_routing(
    lead: dict[str, Any],
    firecrawl_config: FirecrawlConfig,
    apify_config: ApifyEnrichmentConfig,
) -> list[PlannedEnrichmentAction]:
    """Determine provider enrichment routes for a single lead without calling providers."""
    actions: list[PlannedEnrichmentAction] = []

    website = str(lead.get("website") or "").strip()
    instagram = str(lead.get("instagram") or "").strip()
    source_url = str(lead.get("source_url") or "").strip()

    facebook_url = ""
    for candidate in [website, source_url]:
        if "facebook.com" in candidate.lower():
            facebook_url = candidate
            break

    is_custom_website = bool(website and "instagram.com" not in website.lower() and "facebook.com" not in website.lower())
    if is_custom_website:
        actions.append(
            PlannedEnrichmentAction(
                provider="firecrawl",
                target_type="website_pages",
                target_value=website,
                reason="Target website, impressum, contact, and menu pages for business signals",
            )
        )

    has_instagram = bool(instagram or "instagram.com" in website.lower())
    if has_instagram:
        actor = apify_config.instagram_profile_actors[0] if apify_config.instagram_profile_actors else "unregistered_instagram_actor"
        target = instagram or website
        actions.append(
            PlannedEnrichmentAction(
                provider="apify_instagram",
                target_type="instagram_profile",
                target_value=target,
                actor_id=actor,
                reason="Extract profile metadata, bio contact details, and activity signals",
            )
        )

    if facebook_url:
        actor = apify_config.facebook_page_actors[0] if apify_config.facebook_page_actors else "unregistered_facebook_actor"
        actions.append(
            PlannedEnrichmentAction(
                provider="apify_facebook",
                target_type="facebook_page",
                target_value=facebook_url,
                actor_id=actor,
                reason="Extract official business page details, email, and opening hours",
            )
        )

    if not has_instagram and not facebook_url and not is_custom_website:
        actions.append(
            PlannedEnrichmentAction(
                provider="none",
                target_type="no_social_url",
                target_value="",
                status="needs_operator_review",
                reason="No custom website or social URL present; requires operator review or approved search mode",
            )
        )

    if apify_config.people_fallback_actors:
        for actor in apify_config.people_fallback_actors:
            actions.append(
                PlannedEnrichmentAction(
                    provider="apify_people_fallback",
                    target_type="email_phone_fallback",
                    target_value="",
                    actor_id=actor,
                    status="blocked_by_default",
                    reason="People/email/phone fallback actors are blocked by default unless explicitly approved",
                )
            )

    return actions


@dataclass(frozen=True)
class ProviderPlanningSummary:
    leads_inspected: int
    firecrawl_routes: int
    instagram_routes: int
    facebook_routes: int
    people_fallback_blocked: int
    needs_operator_review: int


def format_provider_planning_summary(summary: ProviderPlanningSummary) -> str:
    lines = [
        "=== Provider Enrichment Planning Summary ===",
        f"Leads Inspected:           {summary.leads_inspected}",
        f"Firecrawl Website Routes:  {summary.firecrawl_routes}",
        f"Instagram Actor Routes:    {summary.instagram_routes}",
        f"Facebook Actor Routes:     {summary.facebook_routes}",
        f"People Fallback Blocked:   {summary.people_fallback_blocked}",
        f"Needs Operator Review:     {summary.needs_operator_review}",
    ]
    return "\n".join(lines)


def render_provider_planning_report(
    leads: Sequence[dict[str, Any]],
    firecrawl_config: FirecrawlConfig,
    apify_config: ApifyEnrichmentConfig,
) -> tuple[str, ProviderPlanningSummary]:
    lead_blocks: list[str] = []
    fc_count = 0
    ig_count = 0
    fb_count = 0
    fallback_count = 0
    review_count = 0

    for lead in leads:
        wid = str(lead.get("workflow_id") or "")
        venue = str(lead.get("venue_name") or "(unknown venue)")
        city = str(lead.get("city") or "")
        lines = [
            f"=== Lead: {wid} ===",
            f"Venue: {venue} ({city})",
            "Provider Routing Actions:",
        ]
        actions = plan_lead_provider_routing(lead, firecrawl_config, apify_config)
        if not actions:
            lines.append("  (none)")
        for idx, act in enumerate(actions, start=1):
            lines.append(f"  {idx}. Provider: {act.provider} -> {act.status}")
            lines.append(f"     - Target: {act.target_type} ({act.target_value or 'none'})")
            if act.actor_id:
                lines.append(f"     - Actor ID: {act.actor_id}")
            lines.append(f"     - Reason: {act.reason}")

            if act.provider == "firecrawl":
                fc_count += 1
            elif act.provider == "apify_instagram":
                ig_count += 1
            elif act.provider == "apify_facebook":
                fb_count += 1
            elif act.provider == "apify_people_fallback":
                fallback_count += 1
            elif act.status == "needs_operator_review":
                review_count += 1

        lead_blocks.append("\n".join(lines))

    summary = ProviderPlanningSummary(
        leads_inspected=len(leads),
        firecrawl_routes=fc_count,
        instagram_routes=ig_count,
        facebook_routes=fb_count,
        people_fallback_blocked=fallback_count,
        needs_operator_review=review_count,
    )

    full_output = "\n\n".join(lead_blocks)
    if full_output:
        full_output += "\n\n"
    full_output += format_provider_planning_summary(summary)
    return full_output, summary


def plan_provider_enrichment(
    statuses: Sequence[str] = ("qualified", "needs_review"),
    limit: int = 50,
) -> ProviderPlanningSummary:
    """Read leads from DB and preview provider routing without making network calls."""
    db.ensure_schema()
    leads = db.fetch_leads_for_enrichment_planning(statuses=statuses, limit=limit)
    fc_config = FirecrawlConfig.from_env()
    apify_config = ApifyEnrichmentConfig.from_env()
    report, summary = render_provider_planning_report(leads, fc_config, apify_config)
    print(report)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run planner previewing Firecrawl and Apify social enrichment routing."
    )
    parser.add_argument(
        "--statuses",
        nargs="+",
        default=["qualified", "needs_review"],
        help="Qualification statuses to inspect (default: qualified needs_review)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of leads to inspect (default: 50)",
    )
    args = parser.parse_args()

    try:
        plan_provider_enrichment(statuses=args.statuses, limit=args.limit)
        return 0
    except Exception as error:
        print(f"Provider planning failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
