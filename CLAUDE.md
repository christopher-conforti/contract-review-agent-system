# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running a review

All analysis runs as Claude Code skills — no API key or subprocess required.

| Skill | Purpose |
|---|---|
| `/orchestrate-solidity-review <contract> [spec]` | Full pipeline: all domains → JSON report → email |
| `/analyze-security <contract>` | Reentrancy, overflow, access control, delegatecall |
| `/analyze-efficiency <contract>` | Gas, storage packing, loop costs |
| `/analyze-logic <contract>` | Correctness, invariants, edge cases |
| `/analyze-practices <contract>` | Naming, events, NatSpec, compiler hygiene |
| `/analyze-compliance <contract> <spec>` | Spec deviation against a formal spec |
| `/sync-knowledge` | Populate `knowledge/` from EIP repo, SWC registry, Solidity docs |

## Knowledge base

Skills consult `knowledge/` for authoritative reference material before analyzing:
- `knowledge/eips/` — all Final EIPs
- `knowledge/swc/` — SWC-100 through SWC-136
- `knowledge/solidity/` — security-considerations, common-patterns, units-and-global-variables, known-bugs

Run `/sync-knowledge` once to populate. `knowledge/` content is gitignored; directory structure is tracked via `.gitkeep` files.

## Report schema

`/orchestrate-solidity-review` writes to `reports/<contract_basename>_<YYYYMMDDTHHMMSSz>.json`:

```json
{
  "contract": "...", "spec": "...|null",
  "generated_at": "<ISO 8601 UTC>",
  "requires_human_review": true,
  "summary": { "CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0 },
  "findings": [{
    "domain": "security|efficiency|logic|practices|compliance",
    "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
    "title": "...", "swc": "SWC-NNN|null", "eip_reference": "EIP-N §...|null",
    "location": "...", "description": "...", "fix": "..."
  }]
}
```

## Nix dev shell

```bash
nix develop   # python3, foundry (forge/cast/anvil), solc, slither-analyzer
```

Skills try `slither` and `solc` via Bash before each analysis pass and degrade gracefully when not on PATH. `python3` is used by `knowledge/sync.py` (stdlib only).
