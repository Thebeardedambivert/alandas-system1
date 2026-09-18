"""Environment gates and safe operator output for discovery."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal, InvalidOperation


def _enabled(environment: Mapping[str, str]) -> bool:
    return environment.get("SYSTEM1_DISCOVERY_ENABLED", "false").lower() == "true"


def discovery_enabled(environment: Mapping[str, str]) -> bool:
    """Expose the fail-closed switch without exposing configuration values."""

    return _enabled(environment)


def apify_configured(environment: Mapping[str, str]) -> bool:
    """Return whether Apify has an API token present."""

    return bool(environment.get("APIFY_API_TOKEN", "").strip())


def outscraper_configured(environment: Mapping[str, str]) -> bool:
    """Return whether any Outscraper settings are present."""

    outscraper_keys = (
        "OUTSCRAPER_API_KEY",
        "OUTSCRAPER_WEBHOOK_TOKEN",
        "SYSTEM1_DISCOVERY_OUTSCRAPER_CALLBACK_BASE_URL",
    )
    return any(bool(environment.get(key, "").strip()) for key in outscraper_keys)


def discovery_providers(environment: Mapping[str, str]) -> tuple[str, ...]:
    """Return the selected discovery providers.

    Defaults to ('apify',) when Outscraper is absent/unconfigured.
    Outscraper-only discovery mode is strictly rejected; Apify is required.
    """

    raw = environment.get("SYSTEM1_DISCOVERY_PROVIDERS", "").strip()
    if raw:
        providers = tuple(dict.fromkeys(p.strip().lower() for p in raw.split(",") if p.strip()))
        valid = {"apify", "outscraper"}
        unknown = [p for p in providers if p not in valid]
        if unknown:
            raise RuntimeError(f"unknown discovery provider(s): {', '.join(unknown)}")
        if "apify" not in providers:
            raise RuntimeError("Apify is required for discovery; outscraper-only mode is not supported")
        return providers

    if outscraper_configured(environment):
        return ("apify", "outscraper")
    return ("apify",)


def validate_scheduler_environment(environment: Mapping[str, str]) -> None:
    """Fail closed before a schedule can create a provider request."""

    if not _enabled(environment):
        raise RuntimeError("SYSTEM1_DISCOVERY_ENABLED must be true before discovery can start")

    providers = discovery_providers(environment)
    if "apify" not in providers or not apify_configured(environment):
        raise RuntimeError("missing discovery configuration: APIFY_API_TOKEN")
    _validated_cap(environment, "SYSTEM1_DISCOVERY_MAX_APIFY_USD", Decimal("1.40"))

    if "outscraper" in providers:
        required = (
            "OUTSCRAPER_API_KEY",
            "OUTSCRAPER_WEBHOOK_TOKEN",
            "SYSTEM1_DISCOVERY_OUTSCRAPER_CALLBACK_BASE_URL",
        )
        missing = [name for name in required if not environment.get(name, "").strip()]
        if missing:
            raise RuntimeError("missing discovery configuration: " + ", ".join(missing))
        if len(environment["OUTSCRAPER_WEBHOOK_TOKEN"]) < 32:
            raise RuntimeError("OUTSCRAPER_WEBHOOK_TOKEN must be at least 32 characters")
        _validated_cap(environment, "SYSTEM1_DISCOVERY_MAX_OUTSCRAPER_USD", Decimal("0.60"))


def _validated_cap(environment: Mapping[str, str], name: str, maximum: Decimal) -> Decimal:
    try:
        value = Decimal(environment.get(name, str(maximum)))
    except InvalidOperation as error:
        raise RuntimeError(f"{name} must be a decimal amount") from error
    if value < 0 or value > maximum:
        raise RuntimeError(f"{name} must be between 0 and {maximum}")
    return value


def format_daily_status(run: Mapping[str, str], environment: Mapping[str, str]) -> str:
    """Show state without ever printing secret values or callback URLs."""

    return "\n".join(
        (
            f"Daily run: {run.get('daily_run_id', 'not_started')}",
            f"Status: {run.get('status', 'not_started')}",
            f"Discovery enabled: {'yes' if _enabled(environment) else 'no'}",
            f"Apify configured: {'yes' if apify_configured(environment) else 'no'}",
            f"Outscraper configured: {'yes' if bool(environment.get('OUTSCRAPER_API_KEY', '').strip()) else 'no'}",
        )
    )
