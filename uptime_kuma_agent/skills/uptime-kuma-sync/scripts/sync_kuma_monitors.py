#!/usr/bin/env python3
"""Synchronize Caddy reverse proxy routes into Uptime Kuma as HTTP monitors.

Parses the Caddyfile for configured hostnames, deduplicates them, appends /health
suffixes for MCP service endpoints, and inserts missing monitors directly
into the Uptime Kuma SQLite database.

Usage:
    python sync_kuma_monitors.py [--caddyfile PATH] [--db PATH] [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys


def parse_caddyfile(
    caddyfile_path: str, allowed_suffixes: tuple[str, ...] = ()
) -> list[tuple[str, str]]:
    """Parse Caddyfile and extract (name, url) tuples for each server block.

    Looks for hostname lines followed by ``{``, indicating a Caddy server block
    declaration. When ``allowed_suffixes`` is non-empty, only matching hosts are
    included. Uses any preceding
    `# comment` line as the human-readable monitor name.

    Returns:
        Deduplicated list of (name, url) tuples.
    """
    with open(caddyfile_path) as f:
        lines = f.readlines()

    monitors: list[tuple[str, str]] = []
    current_comment: str | None = None

    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            current_comment = line.lstrip("#").strip()
        elif "{" in line:
            match = re.match(r"(https?://)?([a-zA-Z0-9._-]+)", line)
            if match:
                url = match.group(0)
                hostname = match.group(2).lower()
                if "." not in hostname:
                    continue
                if allowed_suffixes and not any(
                    hostname == suffix or hostname.endswith(f".{suffix}")
                    for suffix in allowed_suffixes
                ):
                    continue
                if not url.startswith("http"):
                    url = "https://" + url if "registry" in url else "http://" + url

                name = current_comment
                if not name:
                    domain_prefix = (
                        url.replace("http://", "").replace("https://", "").split(".")[0]
                    )
                    name = domain_prefix.replace("-", " ").title()

                monitors.append((name, url))
                current_comment = None

    # Deduplicate by URL
    seen: set[str] = set()
    unique: list[tuple[str, str]] = []
    for name, url in monitors:
        if url not in seen:
            seen.add(url)
            unique.append((name, url))
    return unique


def ensure_health_suffix(url: str) -> str:
    """Append /health to MCP service URLs that don't already have it."""
    if "-mcp" in url and not url.endswith("/health"):
        return url + "/health"
    return url


def sync_monitors(
    monitors: list[tuple[str, str]],
    db_path: str,
    dry_run: bool = False,
) -> int:
    """Insert missing monitors into the Uptime Kuma SQLite database.

    Args:
        monitors: List of (name, url) tuples to register.
        db_path: Path to the Uptime Kuma kuma.db file.
        dry_run: If True, print what would be inserted without modifying the DB.

    Returns:
        Number of monitors inserted.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM monitor")
    existing_urls = {row[0] for row in cursor.fetchall()}

    inserted = 0
    for name, url in monitors:
        test_url = ensure_health_suffix(url)

        if test_url in existing_urls:
            print("  [skip] monitor endpoint already registered")
            continue

        if dry_run:
            print(f"  [dry-run] Would register: {name} ({test_url})")
            inserted += 1
            continue

        cursor.execute(
            """
            INSERT INTO monitor (name, url, type, active, user_id, interval,
                                 maxretries, accepted_statuscodes_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (name, test_url, "http", 1, 1, 30, 3, '["200-299"]'),
        )
        print(f"  [added] {name} ({test_url})")
        inserted += 1

    if not dry_run:
        conn.commit()
    conn.close()
    return inserted


def main() -> None:
    configured_caddyfile = os.environ.get("CADDYFILE_PATH")
    configured_db = os.environ.get("KUMA_DB_PATH")
    parser = argparse.ArgumentParser(
        description="Sync Caddy routes into Uptime Kuma monitors."
    )
    parser.add_argument(
        "--caddyfile",
        default=configured_caddyfile,
        required=configured_caddyfile is None,
        help="Path to the Caddyfile (or set CADDYFILE_PATH)",
    )
    parser.add_argument(
        "--db",
        default=configured_db,
        required=configured_db is None,
        help="Path to the Uptime Kuma SQLite database (or set KUMA_DB_PATH)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be inserted without modifying the database.",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.caddyfile):
        print("Error: the configured Caddyfile was not found", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.db):
        print(
            "Error: the configured Uptime Kuma database was not found", file=sys.stderr
        )
        sys.exit(1)

    allowed_suffixes = tuple(
        suffix.strip().lower().lstrip(".")
        for suffix in os.environ.get("MONITOR_HOST_SUFFIXES", "").split(",")
        if suffix.strip()
    )
    monitors = parse_caddyfile(args.caddyfile, allowed_suffixes)
    print(f"Parsed {len(monitors)} routes from Caddyfile.")

    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"Syncing monitors ({mode})...")
    count = sync_monitors(monitors, args.db, dry_run=args.dry_run)

    print(
        f"\nDone. {count} new monitor(s) {'would be' if args.dry_run else ''} registered."
    )


if __name__ == "__main__":
    main()
