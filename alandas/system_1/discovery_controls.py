"""Environment gates and safe operator output for discovery."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal, InvalidOperation


def _enabled(environment: Mapping[str, str]) -> bool:
    return environment.get("SYSTEM1_DISCOVERY_ENABLED", "false").lower() == "true"


def discovery_enabled(environment: Mapping[str, str]) -> bool:
    """Expose the fail-closed switch without exposing configuration values."""

    return _enabled(environment)


def validate_scheduler_environment(environment: Mapping[str, str]) -> None:
    """Fail closed before a schedule can create a provider request."""

    if not _enabled(environment):
        raise RuntimeError("SYSTEM1_DISCOVERY_ENABLED must be true before discovery can start")
    required = (
        "APIFY_API_TOKEN",
        "OUTSCRAPER_API_KEY",
        "OUTSCRAPER_WEBHOOK_TOKEN",
        "SYSTEM1_DISCOVERY_OUTSCRAPER_CALLBACK_BASE_URL",
    )
    missing = [name for name in required if not environment.get(name, "").strip()]
    if missing:
        raise RuntimeError("missing discovery configuration: " + ", ".join(missing))
    if len(environment["OUTSCRAPER_WEBHOOK_TOKEN"]) < 32:
        raise RuntimeError("OUTSCRAPER_WEBHOOK_TOKEN must be at least 32 characters")
    _validated_cap(environment, "SYSTEM1_DISCOVERY_MAX_APIFY_USD", Decimal("1.40"))
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
            f"Apify configured: {'yes' if bool(environment.get('APIFY_API_TOKEN')) else 'no'}",
            f"Outscraper configured: {'yes' if bool(environment.get('OUTSCRAPER_API_KEY')) else 'no'}",
        )
    )
