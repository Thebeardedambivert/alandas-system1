"""Small injectable HTTP boundary for discovery providers."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Protocol
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    json_body: dict[str, object]


class HttpTransport(Protocol):
    def request(
        self, method: str, url: str, headers: dict[str, str], body: bytes | None, timeout_seconds: int
    ) -> HttpResponse: ...


class UrllibHttpTransport:
    """Minimal production transport with a bounded network wait.

    It deliberately does not log request URLs or headers: both can contain a
    callback token or a provider credential.
    """

    def __init__(self, open_request: object = urlopen) -> None:
        self._open_request = open_request

    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: bytes | None,
        timeout_seconds: int,
    ) -> HttpResponse:
        request = Request(url, data=body, headers=headers, method=method)
        with self._open_request(request, timeout=timeout_seconds) as response:
            payload = response.read()
            decoded = json.loads(payload.decode("utf-8")) if payload else {}
            if not isinstance(decoded, dict):
                raise ValueError("provider response must be a JSON object")
            return HttpResponse(response.status, decoded)
