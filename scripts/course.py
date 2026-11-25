#!/usr/bin/env python3
"""Portable commands used by students and by the course documentation."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CAR_SERVICE = ROOT / "apps" / "car-rental-service"
PRICING_SERVICE = ROOT / "apps" / "pricing-service"
WORKFLOWS = ROOT / ".github" / "workflows"

ACTION_SHA = re.compile(r"^[0-9a-f]{40}$")
IMAGE_DIGEST = re.compile(r"@sha256:[0-9a-f]{64}(?:\s|$)")


def run(command: list[str], *, cwd: Path = ROOT) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def gradle_command() -> list[str]:
    if os.name == "nt":
        return ["cmd", "/c", "gradlew.bat"]
    return ["./gradlew"]


def test_java() -> None:
    run([*gradle_command(), "clean", "test"], cwd=CAR_SERVICE)


def test_python() -> None:
    run([sys.executable, "-m", "pytest"], cwd=PRICING_SERVICE)


def test() -> None:
    test_java()
    test_python()


def lint_java() -> None:
    run([*gradle_command(), "checkstyleMain", "checkstyleTest"], cwd=CAR_SERVICE)


def lint_python() -> None:
    run([sys.executable, "-m", "ruff", "check", "app", "tests"], cwd=PRICING_SERVICE)
    run(
        [sys.executable, "-m", "ruff", "format", "--check", "app", "tests"],
        cwd=PRICING_SERVICE,
    )


def lint() -> None:
    lint_java()
    lint_python()


def supply_chain_policy() -> None:
    errors: list[str] = []
    workflows = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])

    for workflow in workflows:
        for line_number, line in enumerate(
            workflow.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.strip()
            if not stripped.startswith("uses:"):
                continue
            reference = stripped.removeprefix("uses:").split("#", maxsplit=1)[0].strip()
            if reference.startswith("./"):
                continue
            if "@" not in reference or not ACTION_SHA.fullmatch(reference.rsplit("@", 1)[1]):
                errors.append(
                    f"{workflow.relative_to(ROOT)}:{line_number}: action not pinned to a SHA"
                )

    for dockerfile in sorted((ROOT / "apps").glob("*/Dockerfile")):
        for line_number, line in enumerate(
            dockerfile.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if line.strip().upper().startswith("FROM ") and not IMAGE_DIGEST.search(line):
                errors.append(
                    f"{dockerfile.relative_to(ROOT)}:{line_number}: base image not pinned to a digest"
                )

    if errors:
        raise RuntimeError("Supply-chain policy failed:\n" + "\n".join(errors))
    print("OK supply-chain policy")


def verify() -> None:
    test()
    lint()
    supply_chain_policy()


def compose_up() -> None:
    require_command("docker")
    run(["docker", "compose", "up", "--build", "--detach"])


def compose_down() -> None:
    require_command("docker")
    run(["docker", "compose", "down"])


def wait_for(url: str, *, timeout_seconds: int = 45) -> None:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=3) as response:
                if 200 <= response.status < 300:
                    print(f"OK {url}")
                    return
        except (URLError, TimeoutError) as error:
            last_error = error
        time.sleep(1)

    raise RuntimeError(f"Service unavailable at {url}: {last_error}")


def smoke() -> None:
    wait_for("http://localhost:8080/health")
    wait_for("http://localhost:8080/cars")
    wait_for("http://localhost:8000/health")
    request = Request(
        "http://localhost:8000/quotes",
        data=json.dumps({"category": "standard", "days": 2}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=3) as response:
        quote = json.load(response)
    if quote.get("total") != 120.0 or quote.get("currency") != "EUR":
        raise RuntimeError(f"Unexpected pricing response: {quote}")
    print("OK pricing quote")


def require_command(command: str) -> None:
    if shutil.which(command) is None:
        raise RuntimeError(f"Required command not found: {command}")


def prerequisites() -> None:
    checks = {
        "Python": sys.executable,
        "Java": shutil.which("java"),
        "Docker": shutil.which("docker"),
    }
    missing = False

    for name, location in checks.items():
        if location:
            print(f"OK {name}: {location}")
        else:
            print(f"MISSING {name}")
            missing = True

    if missing:
        raise RuntimeError("One or more prerequisites are missing")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=[
            "prerequisites",
            "test",
            "test-java",
            "test-python",
            "lint",
            "lint-java",
            "lint-python",
            "supply-chain-policy",
            "verify",
            "compose-up",
            "compose-down",
            "smoke",
        ],
    )
    args = parser.parse_args()

    commands = {
        "prerequisites": prerequisites,
        "test": test,
        "test-java": test_java,
        "test-python": test_python,
        "lint": lint,
        "lint-java": lint_java,
        "lint-python": lint_python,
        "supply-chain-policy": supply_chain_policy,
        "verify": verify,
        "compose-up": compose_up,
        "compose-down": compose_down,
        "smoke": smoke,
    }

    try:
        commands[args.command]()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
