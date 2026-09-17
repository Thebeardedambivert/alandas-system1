"""Bounded public-page research for the free first waterfall stage."""

from __future__ import annotations

import ipaddress
import re
import socket
from html.parser import HTMLParser
from typing import Callable, Iterable
from urllib.error import HTTPError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from system_1.core import instagram_handle
from system_1.models import LeadInput, ResearchEvidence


MAX_PAGES = 6
MAX_RESPONSE_BYTES = 500_000
REQUEST_TIMEOUT_SECONDS = 10
EMAIL_PATTERN = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")


class _NoRedirect(HTTPRedirectHandler):
    """Refuse redirects so every network destination is checked before use."""

    def redirect_request(self, *args: object, **kwargs: object) -> None:
        return None


class _LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value:
                self.hrefs.append(value)


def validate_public_url(
    value: str,
    resolver: Callable[..., list[tuple[object, object, object, object, tuple[str, int]]]] = socket.getaddrinfo,
) -> str:
    """Reject non-web and non-public destinations before a public fetch."""

    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("public research requires an http or https URL with a host")
    if parsed.username or parsed.password:
        raise ValueError("public research URLs cannot contain credentials")
    if parsed.port not in {None, 80, 443}:
        raise ValueError("public research URLs may use only ports 80 or 443")

    try:
        addresses = resolver(parsed.hostname, None, type=socket.SOCK_STREAM)
    except OSError as error:
        raise ValueError(f"could not resolve public research host: {parsed.hostname}") from error
    if not addresses:
        raise ValueError("public research host resolved to no addresses")
    for address in addresses:
        if not ipaddress.ip_address(address[4][0]).is_global:
            raise ValueError("public research host resolved to a non-public address")
    return parsed.geturl()


def candidate_urls(lead: LeadInput) -> list[str]:
    """Return a small, deterministic public-page set for one known website."""

    if not lead.website:
        return []
    base = lead.website.rstrip("/") + "/"
    return [
        base.rstrip("/"),
        urljoin(base, "impressum"),
        urljoin(base, "kontakt"),
        urljoin(base, "contact"),
        urljoin(base, "legal"),
        urljoin(base, "imprint"),
    ]


def fetch_public_page(url: str) -> str:
    """Fetch one small HTML page after its destination has passed validation."""

    safe_url = validate_public_url(url)
    request = Request(safe_url, headers={"User-Agent": "AlandasSystem1Research/1.0"})
    opener = build_opener(_NoRedirect())
    try:
        with opener.open(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"text/html", "text/plain"}:
                raise ValueError(f"unsupported public research content type: {content_type}")
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except HTTPError as error:
        raise ValueError(f"public research request failed with HTTP {error.code}") from error
    if len(body) > MAX_RESPONSE_BYTES:
        raise ValueError("public research page exceeded the size limit")
    return body.decode("utf-8", errors="replace")


def extract_evidence(html: str, source_url: str) -> list[ResearchEvidence]:
    """Extract only public business contact routes and their evidence source."""

    collector = _LinkCollector()
    collector.feed(html)
    findings: list[ResearchEvidence] = []
    emails = set(EMAIL_PATTERN.findall(html))
    for href in collector.hrefs:
        if href.lower().startswith("mailto:"):
            emails.add(unquote(href[7:].split("?", 1)[0]))
    for email in sorted(email.strip().lower() for email in emails if "@" in email):
        findings.append(ResearchEvidence("email", email, source_url, "public_page"))

    for href in collector.hrefs:
        lowered = href.lower()
        if lowered.startswith("tel:"):
            number = unquote(href[4:]).strip()
            if number:
                findings.append(ResearchEvidence("phone", number, source_url, "public_page"))
        parsed = urlparse(href)
        if parsed.hostname and parsed.hostname.lower().removeprefix("www.") == "instagram.com":
            handle = instagram_handle(href)
            if handle:
                findings.append(ResearchEvidence("instagram", handle, source_url, "public_page"))

    if "/impressum" in urlparse(source_url).path.lower():
        findings.append(ResearchEvidence("impressum_url", source_url, source_url, "public_impressum"))
    return _unique_findings(findings)


def research_public_pages(
    lead: LeadInput, fetcher: Callable[[str], str] = fetch_public_page
) -> tuple[list[ResearchEvidence], list[str]]:
    """Research a bounded public page set without calling paid providers."""

    findings: list[ResearchEvidence] = []
    notes: list[str] = []
    for url in candidate_urls(lead)[:MAX_PAGES]:
        try:
            html = fetcher(url)
        except ValueError as error:
            notes.append(f"Public research skipped {url}: {error}")
            continue
        findings.extend(extract_evidence(html, url))
    if not candidate_urls(lead):
        notes.append("Website missing; public website research cannot start")
    return _unique_findings(findings), notes


def _unique_findings(findings: Iterable[ResearchEvidence]) -> list[ResearchEvidence]:
    seen: set[tuple[str, str, str]] = set()
    output: list[ResearchEvidence] = []
    for finding in findings:
        key = (finding.field, finding.value.lower(), finding.source_url)
        if key not in seen:
            seen.add(key)
            output.append(finding)
    return output
