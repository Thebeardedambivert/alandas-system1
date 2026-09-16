"""Tests for pure Alandas System 1 lead logic."""

from __future__ import annotations

import unittest

from system_1.core import draft_outreach, enrich_lead, lead_workflow_id, slug, validate_lead
from system_1.models import LeadInput


class System1CoreTests(unittest.TestCase):
    def test_valid_lead_passes(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
            fit_score=4,
        )

        self.assertEqual(validate_lead(lead), [])

    def test_missing_contact_route_fails(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
        )

        self.assertIn("at least one contact route is required", validate_lead(lead))

    def test_fit_score_range_is_checked(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
            fit_score=6,
        )

        self.assertIn("fit_score must be between 1 and 5", validate_lead(lead))

    def test_enrichment_lists_missing_research(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
        )

        notes = enrich_lead(lead)

        self.assertIn("Find public Impressum or contact page", notes)
        self.assertIn("Find email from website, Impressum, or approved tool", notes)

    def test_draft_requires_sidy_approval(self) -> None:
        lead = LeadInput(
            venue_name="Example Cafe",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
        )

        draft = draft_outreach(lead)

        self.assertFalse(draft.allowed_to_send)
        self.assertIn("EUR 19 discovery box", draft.body)

    def test_lead_workflow_id_is_stable(self) -> None:
        lead = LeadInput(
            venue_name="Cafe Beispiel Mitte",
            city="Berlin",
            venue_type="cafe",
            source_url="https://example.de",
            website="https://example.de",
        )

        self.assertEqual(lead_workflow_id(lead), "alandas-lead-berlin-cafe-beispiel-mitte")

    def test_slug_handles_empty_values(self) -> None:
        self.assertEqual(slug("   "), "lead")


if __name__ == "__main__":
    unittest.main()
