"""Offline translation for the approved Apify Google Maps actor dataset.

This module deliberately has no HTTP client and no Apify token support. It
accepts already-exported actor results, so mapping can be tested before a paid
run is approved.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from system_1.core import normalize_lead
from system_1.models import DiscoveryCandidate, LeadInput


SOURCE_NAME = "apify_google_maps"
ALLOWED_CITIES = frozenset({"berlin", "hamburg", "munich"})
MAX_RESULTS_PER_RUN = 50


def validate_discovery_request(city: str, search_terms: Sequence[str], limit: int) -> list[str]:
    """Validate the small, approved shape of a future discovery run."""

    errors: list[str] = []
    if city.strip().lower() not in ALLOWED_CITIES:
        errors.append("city must be one of Berlin, Hamburg, or Munich")
    if not search_terms or any(not term.strip() for term in search_terms):
        errors.append("at least one non-blank search term is required")
    if not 1 <= limit <= MAX_RESULTS_PER_RUN:
        errors.append(f"limit must be between 1 and {MAX_RESULTS_PER_RUN}")
    return errors


def map_apify_place(record: Mapping[str, Any]) -> DiscoveryCandidate | None:
    """Map one documented actor place row; reject ads and closed businesses."""

    if record.get("isAdvertisement") is True:
        return None
    if record.get("permanentlyClosed") is True or record.get("temporarilyClosed") is True:
        return None

    source_record_id = _text(record.get("placeId"))
    source_url = _text(record.get("url"))
    venue_name = _text(record.get("title"))
    city = _text(record.get("city"))
    venue_type = _text(record.get("categoryName"))
    country_code = _text(record.get("countryCode")).upper()
    required = {
        "placeId": source_record_id,
        "url": source_url,
        "title": venue_name,
        "city": city,
        "categoryName": venue_type,
        "countryCode": country_code,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise ValueError(f"Apify place is missing required fields: {', '.join(missing)}")
    if country_code != "DE":
        raise ValueError("Apify place must have countryCode DE")
    if not source_url.startswith(("http://", "https://")):
        raise ValueError("Apify place url must be an http or https URL")

    return DiscoveryCandidate(
        source=SOURCE_NAME,
        source_record_id=source_record_id,
        source_url=source_url,
        venue_name=venue_name,
        city=city,
        venue_type=venue_type,
        country_code=country_code,
        website=_text(record.get("website")),
        phone=_text(record.get("phoneUnformatted")) or _text(record.get("phone")),
        address=_text(record.get("address")),
    )


def candidate_to_lead(candidate: DiscoveryCandidate) -> LeadInput:
    """Create a raw lead without importing paid add-on contact enrichment."""

    if candidate.source != SOURCE_NAME:
        raise ValueError(f"unsupported discovery source: {candidate.source}")
    return normalize_lead(
        LeadInput(
            venue_name=candidate.venue_name,
            city=candidate.city,
            venue_type=candidate.venue_type,
            source_url=candidate.source_url,
            website=candidate.website,
            phone=candidate.phone,
        )
    )


def map_apify_dataset(records: Sequence[Mapping[str, Any]]) -> tuple[list[DiscoveryCandidate], list[str]]:
    """Map a bounded actor export and surface skipped rows for human review."""

    if len(records) > MAX_RESULTS_PER_RUN:
        raise ValueError(f"dataset exceeds the {MAX_RESULTS_PER_RUN}-result review limit")
    candidates: list[DiscoveryCandidate] = []
    notes: list[str] = []
    seen_place_ids: set[str] = set()
    for index, record in enumerate(records, start=1):
        try:
            candidate = map_apify_place(record)
        except ValueError as error:
            notes.append(f"row {index}: skipped: {error}")
            continue
        if candidate is None:
            notes.append(f"row {index}: skipped: advertisement or closed business")
            continue
        if candidate.source_record_id in seen_place_ids:
            notes.append(f"row {index}: skipped: duplicate Google Place ID")
            continue
        seen_place_ids.add(candidate.source_record_id)
        candidates.append(candidate)
    return candidates, notes


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""
