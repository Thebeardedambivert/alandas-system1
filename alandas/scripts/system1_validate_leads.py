"""Validate Alandas System 1 lead CSV files.

The script is offline by design. It checks structure and obvious data mistakes
before any outreach draft is sent to Sidy.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "venue_name",
    "city",
    "venue_type",
    "website",
    "instagram",
    "email",
    "phone",
    "impressum_url",
    "decision_maker",
    "seat_estimate",
    "fit_score",
    "fit_reason",
    "source_url",
    "status",
    "next_action",
]

NON_EMPTY_FIELDS = [
    "venue_name",
    "city",
    "venue_type",
    "fit_score",
    "fit_reason",
    "source_url",
    "status",
    "next_action",
]

ALLOWED_STATUSES = {
    "new",
    "needs_research",
    "qualified",
    "drafted",
    "sent_to_sidy",
    "approved",
    "contacted",
    "rejected",
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_url(value: str) -> bool:
    return not value or value.startswith(("http://", "https://"))


def validate_row(row_number: int, row: dict[str, str]) -> list[str]:
    errors: list[str] = []

    for field in NON_EMPTY_FIELDS:
        if not row.get(field, "").strip():
            errors.append(f"row {row_number}: {field} is required")

    contact_values = [
        row.get("email", "").strip(),
        row.get("phone", "").strip(),
        row.get("instagram", "").strip(),
        row.get("website", "").strip(),
    ]
    if not any(contact_values):
        errors.append(f"row {row_number}: at least one contact route is required")

    for field in ["website", "instagram", "impressum_url", "source_url"]:
        value = row.get(field, "").strip()
        if not is_url(value):
            errors.append(f"row {row_number}: {field} must start with http:// or https://")

    email = row.get("email", "").strip()
    if email and not EMAIL_RE.match(email):
        errors.append(f"row {row_number}: email is invalid")

    fit_score_raw = row.get("fit_score", "").strip()
    try:
        fit_score = int(fit_score_raw)
    except ValueError:
        errors.append(f"row {row_number}: fit_score must be an integer from 1 to 5")
    else:
        if fit_score < 1 or fit_score > 5:
            errors.append(f"row {row_number}: fit_score must be between 1 and 5")

    status = row.get("status", "").strip()
    if status and status not in ALLOWED_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_STATUSES))
        errors.append(f"row {row_number}: status must be one of: {allowed}")

    return errors


def validate_csv(path: Path) -> list[str]:
    if not path.exists():
        return [f"file does not exist: {path}"]

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            return ["CSV has no header row"]

        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            return [f"CSV is missing columns: {', '.join(missing)}"]

        errors: list[str] = []
        row_count = 0
        for row_count, row in enumerate(reader, start=2):
            errors.extend(validate_row(row_count, row))

        if row_count == 0:
            errors.append("CSV has no lead rows")

        return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/system1_validate_leads.py path/to/leads.csv")
        return 2

    path = Path(sys.argv[1])
    errors = validate_csv(path)
    if errors:
        print("System 1 lead validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"System 1 lead validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
