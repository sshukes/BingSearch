#!/usr/bin/env python3
"""Bing search bot using Playwright with a persistent profile.

This keeps searches associated with the signed-in account by reusing the
browser profile directory between runs.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import time
from typing import Iterable

from playwright.sync_api import sync_playwright

DEFAULT_QUERY_FILE = "queries.txt"
DEFAULT_PROFILE_DIR = ".bing-profile"
DEFAULT_DELAY = 3.0


def load_queries(path: pathlib.Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Query file not found: {path}")

    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    return [line for line in lines if line]


def run_searches(queries: Iterable[str], profile_dir: pathlib.Path, delay_s: float) -> None:
    profile_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
        )
        page = browser.new_page()

        try:
            page.goto("https://www.bing.com", wait_until="domcontentloaded")
            for query in queries:
                page.fill("input[name='q']", query)
                page.keyboard.press("Enter")
                page.wait_for_load_state("domcontentloaded")
                time.sleep(delay_s)
        finally:
            browser.close()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Bing searches using a persistent profile.",
    )
    parser.add_argument(
        "--queries",
        default=DEFAULT_QUERY_FILE,
        help="Path to a newline-delimited query file.",
    )
    parser.add_argument(
        "--profile-dir",
        default=DEFAULT_PROFILE_DIR,
        help="Directory for the persistent browser profile.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help="Delay in seconds between searches.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    query_path = pathlib.Path(args.queries)
    profile_dir = pathlib.Path(args.profile_dir)

    queries = load_queries(query_path)
    if not queries:
        print("No queries found. Add at least one query.")
        return 1

    run_searches(queries, profile_dir, args.delay)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
