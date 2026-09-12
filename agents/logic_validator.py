"""Logic Validator agent: checks Solidity contract logic for correctness.

Focus areas: algorithm correctness, edge cases, and invariant violations.
"""

import json

import anthropic

import config

SYSTEM_PROMPT = """You are a smart contract logic validator. You review Solidity \
code for correctness issues and respond with JSON only — no markdown, no preamble, \
no explanation outside the JSON structure.

Focus exclusively on these categories:
- Algorithm correctness (off-by-one errors, incorrect arithmetic, wrong conditionals)
- Edge cases (zero values, empty arrays, boundary conditions, first/last iterations)
- Invariants (conditions that should always hold, e.g. total supply consistency,
  balance conservation) and whether the code could violate them

Do not comment on security exploits, gas efficiency, or code style — those are \
handled by other agents. Only flag a logic issue when the code's actual behavior \
diverges from its evident intent.

Respond with a single JSON object matching this exact shape:
{
  "agent": "logic_validator",
  "findings": [
    {
      "type": "algorithm_correctness | edge_case | invariant_violation",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "location": "function or line reference",
      "description": "what the logic issue is",
      "failure_scenario": "concrete input or sequence that triggers the incorrect behavior",
      "recommended_fix": "concrete fix"
    }
  ]
}

If no issues are found, return {"agent": "logic_validator", "findings": []}."""


def analyze(contract_code: str) -> dict:
    """Run the logic validator agent against Solidity source and return parsed JSON findings."""
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    response = client.messages.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": contract_code}],
    )

    raw_text = response.content[0].text

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        return {
            "agent": "logic_validator",
            "findings": [],
            "error": f"Failed to parse agent response as JSON: {exc}",
            "raw_response": raw_text,
        }
