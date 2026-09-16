"""Print a Coolify-ready System 1 environment block with random passwords."""

from __future__ import annotations

import secrets
import string


ALPHABET = string.ascii_letters + string.digits


def token(length: int = 40) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def main() -> None:
    postgres_password = token()
    temporal_password = token()

    print("POSTGRES_USER=alandas")
    print(f"POSTGRES_PASSWORD={postgres_password}")
    print("POSTGRES_DB=alandas_system1")
    print()
    print("TEMPORAL_POSTGRES_USER=temporal")
    print(f"TEMPORAL_POSTGRES_PASSWORD={temporal_password}")
    print("TEMPORAL_POSTGRES_DB=temporal")
    print()
    print("TEMPORAL_VERSION=1.27.2")
    print("TEMPORAL_ADMINTOOLS_VERSION=1.32.0")
    print("TEMPORAL_UI_VERSION=2.39.0")
    print("TEMPORAL_ADDRESS=temporal:7233")
    print("TEMPORAL_NAMESPACE=default")
    print("TEMPORAL_TASK_QUEUE=alandas-system1")
    print("TEMPORAL_CORS_ORIGINS=http://localhost:8080")
    print()
    print("LOG_LEVEL=info")


if __name__ == "__main__":
    main()
