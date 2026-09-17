"""Safe translation of basic Outscraper Google Maps results.

This module accepts only the ordinary place fields needed to begin Alandas'
existing research waterfall.  It deliberately ignores Outscraper enrichment,
reviews, social data, and any personal-contact data.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from system_1.apify_google_maps import MAX_RESULTS_PER_RUN
from system_1.core import normalize_lead
from system_1.models import DiscoveryCandidate, LeadInput


SOURCE_NAME = "outscraper_google_maps"


def map_outscraper_place(record: Mapping[str, Any]) -> DiscoveryCandidate | None:
    """Translate one documented Maps result or reject an unsuitable row."""

    if record.get("is_ad") is True or record.get("isAdvertisement") is True:
        return None
    if _text(record.get("business_status")).upper() in {
        "CLOSED_PERMANENTLY",
        "CLOSED_TEMPORARILY",
    }:
        return None

    source_record_id = _text(record.get("place_id"))
    source_url = _text(record.get("location_link"))
    if not source_url and source_record_id:
        source_url = f"https://www.google.com/maps/place/?q=place_id:{source_record_id}"
    venue_name = _text(record.get("name"))
    city = _text(record.get("city"))
    venue_type = _text(record.get("type")) or _text(record.get("category"))
    country_code = _text(record.get("country_code")).upper()
    required = {
        "place_id": source_record_id,
        "name": venue_name,
        "city": city,
        "type": venue_type,
        "country_code": country_code,
        "location_link": source_url,
    }
    missing = [field for field, value in required.items() if not value]
    if missing:
        raise ValueError(
            "Outscraper place is missing required fields: " + ", ".join(missing)
        )
    if country_code != "DE":
        raise ValueError("Outscraper place must have country_code DE")
    return DiscoveryCandidate(
        source=SOURCE_NAME,
        source_record_id=source_record_id,
        source_url=source_url,
        venue_name=venue_name,
        city=city,
        venue_type=venue_type,
        country_code=country_code,
        website=_text(record.get("site")),
        phone=_text(record.get("phone")),
        address=_text(record.get("full_address")),
    )


def callback_records(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """Flatten Outscraper's documented one-query or multi-query ``data`` shape."""

    data = payload.get("data")
    if not isinstance(data, list):
        raise ValueError("Outscraper callback data must be a list")
    records: list[Mapping[str, Any]] = []
    for group in data:
        if isinstance(group, Mapping):
            records.append(group)
        elif isinstance(group, list):
            records.extend(item for item in group if isinstance(item, Mapping))
        else:
            raise ValueError("Outscraper callback data contains an invalid result group")
    if len(records) > MAX_RESULTS_PER_RUN:
        raise ValueError(
            f"Outscraper callback exceeds the {MAX_RESULTS_PER_RUN}-result review limit"
        )
    return records


def map_outscraper_callback(
    payload: Mapping[str, Any],
) -> tuple[list[DiscoveryCandidate], list[str]]:
    """Map a bounded callback and retain non-sensitive skip reasons."""

    if _text(payload.get("status")).lower() != "success":
        raise ValueError("Outscraper callback status must be Success")
    candidates: list[DiscoveryCandidate] = []
    notes: list[str] = []
    seen_place_ids: set[str] = set()
    for index, record in enumerate(callback_records(payload), start=1):
        try:
            candidate = map_outscraper_place(record)
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


def candidate_to_lead(candidate: DiscoveryCandidate) -> LeadInput:
    """Create the raw lead that enters the existing System 1 workflow."""

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


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""
