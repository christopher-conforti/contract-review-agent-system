# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Primary implementation: Claude Code skills

The skills in `.claude/commands/` are the primary implementation. They run directly inside Claude Code — no API key or subprocess required.

| Skill | Purpose |
|---|---|
| `/orchestrate-solidity-review <contract> [spec]` | Full pipeline: all domains → JSON report → email |
| `/analyze-security <contract>` | Reentrancy, overflow, access control, delegatecall |
| `/analyze-efficiency <contract>` | Gas, storage packing, loop costs |
| `/analyze-logic <contract>` | Correctness, invariants, edge cases |
| `/analyze-practices <contract>` | Naming, events, NatSpec, compiler hygiene |
| `/analyze-compliance <contract> <spec>` | Spec deviation against a formal spec |
| `/sync-knowledge` | Populate `knowledge/` from EIP repo, SWC registry, Solidity docs |

### Knowledge base

Before analyzing, skills consult `knowledge/` for authoritative reference material:
- `knowledge/eips/` — all Final EIPs (fetched from ethereum/EIPs)
- `knowledge/swc/` — SWC-100 through SWC-136 weakness entries
- `knowledge/solidity/` — security-considerations, common-patterns, units-and-global-variables, known-bugs

Run `/sync-knowledge` once to populate. Re-run to pick up new upstream content. `knowledge/` content is gitignored; directory structure is tracked via `.gitkeep` files.

### Reports

`/orchestrate-solidity-review` writes JSON to `reports/<contract_basename>_<YYYYMMDDTHHMMSSz>.json` and self-sends an email summary via MoltMail.

Report schema:
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

## Legacy Python orchestrator

`orchestrator.py` and `agents/` contain a Python implementation that calls the Anthropic API directly. It requires `ANTHROPIC_API_KEY` and `pip install -r requirements.txt`. It is retained for reference but the skills are preferred.

## Nix dev shell

```bash
nix develop   # Python + anthropic, foundry (forge/cast/anvil), solc, slither-analyzer
```

Skills automatically try `slither` and `solc` via Bash before each analysis pass and degrade gracefully when not on PATH.
