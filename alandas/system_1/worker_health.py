"""Safe operator health check for System 1 worker dependencies."""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
import os
import socket
import sys

from system_1.discovery_controls import apify_configured, discovery_enabled


def check_socket_connectivity(host: str, port: int, timeout_seconds: float = 3.0) -> tuple[bool, str]:
    """Test TCP socket connection to a target host/port."""
    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return True, "connected"
    except Exception as error:
        return False, str(error)


def parse_host_port(address: str, default_port: int = 7233) -> tuple[str, int]:
    """Parse host and port from address string like host:port."""
    address = address.strip()
    if not address:
        return "localhost", default_port
    if ":" in address:
        parts = address.rsplit(":", 1)
        try:
            return parts[0], int(parts[1])
        except ValueError:
            return parts[0], default_port
    return address, default_port


def check_db_connectivity(database_url: str | None) -> tuple[bool, str]:
    """Verify Postgres connection without exposing credentials."""
    if not database_url:
        return False, "DATABASE_URL not set"
    try:
        import psycopg
        with psycopg.connect(database_url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return True, "connected"
    except Exception as error:
        return False, f"error: {error.__class__.__name__}"


async def check_temporal_client_connectivity(address: str, namespace: str) -> tuple[bool, str]:
    """Attempt a direct Temporal client connection."""
    try:
        from temporalio.client import Client
        await Client.connect(address, namespace=namespace)
        return True, "connected"
    except Exception as error:
        return False, f"error: {error.__class__.__name__}"


def format_worker_health(
    environment: Mapping[str, str],
    *,
    db_status: tuple[bool, str],
    temporal_socket_status: tuple[bool, str],
    temporal_client_status: tuple[bool, str],
) -> str:
    """Format worker health report without exposing secrets."""
    address = environment.get("TEMPORAL_ADDRESS", "localhost:7233")
    namespace = environment.get("TEMPORAL_NAMESPACE", "default")
    task_queue = environment.get("TEMPORAL_TASK_QUEUE", "alandas-system1")

    lines = [
        "=== System 1 Worker Health ===",
        f"Database connectivity: {'ok' if db_status[0] else 'failed'} ({db_status[1]})",
        f"Temporal address: {address}",
        f"Temporal socket connectivity: {'ok' if temporal_socket_status[0] else 'failed'} ({temporal_socket_status[1]})",
        f"Temporal client connectivity: {'ok' if temporal_client_status[0] else 'failed'} ({temporal_client_status[1]})",
        f"Temporal namespace: {namespace}",
        f"Temporal task queue: {task_queue}",
        f"Discovery enabled: {'yes' if discovery_enabled(environment) else 'no'}",
        f"Apify configured: {'yes' if apify_configured(environment) else 'no'}",
        f"Outscraper configured: {'yes' if bool(environment.get('OUTSCRAPER_API_KEY', '').strip()) else 'no'}",
    ]
    all_ok = db_status[0] and temporal_client_status[0]
    lines.append(f"Overall status: {'healthy' if all_ok else 'degraded'}")
    return "\n".join(lines)


async def main() -> int:
    env = os.environ
    db_url = env.get("DATABASE_URL")
    db_status = check_db_connectivity(db_url)

    temporal_address = env.get("TEMPORAL_ADDRESS", "localhost:7233")
    namespace = env.get("TEMPORAL_NAMESPACE", "default")
    host, port = parse_host_port(temporal_address, 7233)
    socket_status = check_socket_connectivity(host, port)

    client_status = await check_temporal_client_connectivity(temporal_address, namespace)

    output = format_worker_health(
        env,
        db_status=db_status,
        temporal_socket_status=socket_status,
        temporal_client_status=client_status,
    )
    print(output)
    return 0 if (db_status[0] and client_status[0]) else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
