# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the system

```bash
export ANTHROPIC_API_KEY=<your-key>
pip install -r requirements.txt

# Without spec
python orchestrator.py --contract test_contracts/vulnerable.sol

# With spec
python orchestrator.py --contract test_contracts/simple_erc20.sol --spec test_contracts/specs/erc20_spec.md
```

Reports are written to `reports/<contract_name>_<timestamp>.json`.

## Architecture

The orchestrator (`orchestrator.py`) is the entry point. It reads a `.sol` file (and optional spec), calls five specialized agents sequentially, consolidates their findings, and writes a unified JSON report.

Each agent in `agents/` follows the same pattern:
- A scoped `SYSTEM_PROMPT` that constrains the agent to a single concern and demands pure JSON output
- A single `analyze(contract_code, ...)` function that calls the Anthropic API and returns a parsed dict with shape `{"agent": "<name>", "findings": [...]}`
- JSON parse errors surface as an `"error"` key instead of raising, so the orchestrator can continue

The `spec_compliance` agent is the only one with a different signature — it takes `(contract_code, spec)` and is only invoked when `--spec` is provided.

The orchestrator's `consolidate()` function merges all agent results, tags each finding with its source agent, sorts by severity (`CRITICAL → HIGH → MEDIUM → LOW`), and sets `requires_human_review: true` when any CRITICAL or HIGH findings exist.

## Agent output contract

Every agent must return:
```json
{
  "agent": "<agent_name>",
  "findings": [
    {
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      ...agent-specific fields...
    }
  ]
}
```

Adding a new agent: implement `analyze()` returning the above shape, then register it in `orchestrator.py`'s `run_agents()`.

## Config

`config.py` reads `ANTHROPIC_API_KEY` from the environment. `MODEL` and `MAX_TOKENS` are set there and shared by all agents — change them in one place.
