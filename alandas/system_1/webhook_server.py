"""Small HTTP ingress for approved discovery-provider callbacks."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from system_1.db import ensure_schema
from system_1.outscraper_webhook import receive_outscraper_callback, temporal_workflow_starter


MAX_BODY_BYTES = 1_048_576
OUTSCRAPER_PATH = "/webhooks/outscraper/google-maps"
logger = logging.getLogger(__name__)


class WebhookHandler(BaseHTTPRequestHandler):
    """Serve health checks and the single configured discovery callback."""

    server_version = "AlandasWebhook/1"

    def do_GET(self) -> None:  # noqa: N802
        if urlparse(self.path).path == "/healthz":
            self._reply(HTTPStatus.OK, {"status": "ok"})
        else:
            self._reply(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != OUTSCRAPER_PATH:
            self._reply(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        if os.environ.get("SYSTEM1_OUTSCRAPER_WEBHOOK_ENABLED", "false").lower() != "true":
            self._reply(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "webhook disabled"})
            return
        content_length = self.headers.get("Content-Length", "")
        try:
            size = int(content_length)
        except ValueError:
            self._reply(HTTPStatus.LENGTH_REQUIRED, {"error": "content length required"})
            return
        if size < 1 or size > MAX_BODY_BYTES:
            self._reply(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "invalid body size"})
            return
        if self.headers.get("Content-Type", "").split(";", 1)[0].lower() != "application/json":
            self._reply(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "application/json required"})
            return
        try:
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise ValueError("JSON object required")
            token = parse_qs(parsed.query).get("token", [""])[0]
            result = asyncio.run(_receive(payload, token))
        except PermissionError:
            self._reply(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
        except ValueError as error:
            self._reply(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except Exception:
            logger.exception("Outscraper webhook processing failed")
            self._reply(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "callback processing failed"})
        else:
            self._reply(HTTPStatus.ACCEPTED, result)

    def log_message(self, format: str, *args: object) -> None:
        """Avoid recording callback URLs, tokens, or request bodies in logs."""

        logger.info("webhook request completed: %s", args[1] if len(args) > 1 else "")

    def _reply(self, status: HTTPStatus, body: dict[str, object]) -> None:
        encoded = json.dumps(body, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


async def _receive(payload: dict[str, object], token: str) -> dict[str, object]:
    from temporalio.client import Client

    address = os.environ.get("TEMPORAL_ADDRESS", "temporal:7233")
    namespace = os.environ.get("TEMPORAL_NAMESPACE", "default")
    queue = os.environ.get("TEMPORAL_TASK_QUEUE", "alandas-system1")
    client = await Client.connect(address, namespace=namespace)
    return await receive_outscraper_callback(
        payload,
        provided_token=token,
        expected_token=os.environ.get("OUTSCRAPER_WEBHOOK_TOKEN", ""),
        start_workflow=temporal_workflow_starter(client, queue),
    )


def main() -> None:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "info").upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    ensure_schema()
    port = int(os.environ.get("SYSTEM1_WEBHOOK_PORT", "8080"))
    server = ThreadingHTTPServer(("", port), WebhookHandler)
    logger.info("Webhook ingress listening on port %s", port)
    server.serve_forever()


if __name__ == "__main__":
    main()
