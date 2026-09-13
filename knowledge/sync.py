#!/usr/bin/env python3
"""Sync global knowledge base: finalized EIPs, SWC registry, Solidity security docs.

Writes to ~/.claude/knowledge/{eips,swc,solidity}/ — shared across all projects.

Usage:
    python3 knowledge/sync.py          # skip already-cached files
    python3 knowledge/sync.py --force  # re-download everything
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path.home() / ".claude" / "knowledge"
FORCE = "--force" in sys.argv
HEADERS = {"User-Agent": "contract-review-kb/1.0"}


def get(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def save(url: str, dest: Path, keep_if: callable = None) -> str:
    """Fetch url and write to dest. keep_if(text) gates writes; skipped files are not saved."""
    if not FORCE and dest.exists():
        return "cached"
    try:
        data = get(url)
        if keep_if and not keep_if(data.decode(errors="replace")):
            return "skipped"
        dest.write_bytes(data)
        return "fetched"
    except Exception as exc:
        return f"error: {exc}"


# ── EIPs ──────────────────────────────────────────────────────────────────────

def sync_eips() -> None:
    eip_dir = ROOT / "eips"
    eip_dir.mkdir(parents=True, exist_ok=True)

    print("EIPs  fetching file list…")
    try:
        listing = json.loads(get(
            "https://api.github.com/repos/ethereum/EIPs/contents/EIPS",
            timeout=30,
        ))
    except Exception as exc:
        print(f"      error fetching listing: {exc}")
        return

    if isinstance(listing, dict) and "message" in listing:
        print(f"      GitHub API error: {listing['message']}")
        return

    candidates = [
        f["name"] for f in listing
        if f["name"].startswith("eip-") and f["name"].endswith(".md")
    ]
    print(f"      {len(candidates)} candidates — downloading, filtering to Final…")

    counts = {"fetched": 0, "cached": 0, "skipped": 0, "error": 0}
    for name in candidates:
        url = f"https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/{name}"
        result = save(url, eip_dir / name, keep_if=lambda t: "status: Final" in t)
        key = result if result in counts else "error"
        counts[key] += 1
        if result == "fetched":
            time.sleep(0.05)

    print(
        f"      fetched={counts['fetched']}  cached={counts['cached']}  "
        f"non-Final skipped={counts['skipped']}  errors={counts['error']}"
    )


# ── SWC ───────────────────────────────────────────────────────────────────────

def sync_swc() -> None:
    swc_dir = ROOT / "swc"
    swc_dir.mkdir(parents=True, exist_ok=True)
    base = "https://raw.githubusercontent.com/SmartContractSecurity/SWC-registry/master"

    print("SWC   syncing registry…")
    result = save(f"{base}/README.md", swc_dir / "README.md")
    print(f"      README: {result}")

    for n in range(100, 137):
        result = save(f"{base}/entries/docs/SWC-{n}.md", swc_dir / f"SWC-{n}.md")
        if result != "cached":
            print(f"      SWC-{n}: {result}")

    print("      done")


# ── Solidity ──────────────────────────────────────────────────────────────────

def sync_solidity() -> None:
    sol_dir = ROOT / "solidity"
    sol_dir.mkdir(parents=True, exist_ok=True)
    base = "https://raw.githubusercontent.com/ethereum/solidity/develop/docs"

    docs = [
        ("security-considerations.rst", "security-considerations.rst"),
        ("common-patterns.rst",          "common-patterns.rst"),
        ("units-and-global-variables.rst", "units-and-global-variables.rst"),
        ("bugs.json",                    "known-bugs.json"),
    ]
    print("Solidity  syncing docs…")
    for src, dst in docs:
        result = save(f"{base}/{src}", sol_dir / dst)
        print(f"          {dst}: {result}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    label = " (--force: re-downloading all)" if FORCE else ""
    print(f"Syncing knowledge base{label}…\n")
    sync_eips()
    print()
    sync_swc()
    print()
    sync_solidity()
    print("\nKnowledge base up to date.")
    print(f"  EIPs:     {ROOT}/eips/")
    print(f"  SWC:      {ROOT}/swc/")
    print(f"  Solidity: {ROOT}/solidity/")
