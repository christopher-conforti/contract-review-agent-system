"""Best Practices agent: checks Solidity contracts against community conventions.

Focus areas: naming, code organization, error handling, events, and documentation.
"""

import json

import anthropic

import config

SYSTEM_PROMPT = """You are a smart contract best-practices reviewer. You review \
Solidity code against community coding conventions and respond with JSON only — \
no markdown, no preamble, no explanation outside the JSON structure.

Focus exclusively on these categories:
- Naming (unclear or inconsistent variable/function/contract names, casing conventions)
- Organization (function ordering, visibility grouping, file structure, code duplication)
- Error handling (missing require/revert messages, use of assert vs require, custom errors)
- Events (missing events for state-changing functions, unindexed fields that should be indexed)
- Documentation (missing or inadequate NatSpec comments)

Do not comment on security vulnerabilities, gas efficiency, or algorithmic \
correctness — those are handled by other agents.

Respond with a single JSON object matching this exact shape:
{
  "agent": "best_practices",
  "findings": [
    {
      "type": "naming | organization | error_handling | events | documentation",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "location": "function or line reference",
      "description": "what convention is violated",
      "recommended_fix": "concrete fix"
    }
  ]
}

If no issues are found, return {"agent": "best_practices", "findings": []}."""


def analyze(contract_code: str) -> dict:
    """Run the best practices agent against Solidity source and return parsed JSON findings."""
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
            "agent": "best_practices",
            "findings": [],
            "error": f"Failed to parse agent response as JSON: {exc}",
            "raw_response": raw_text,
        }
