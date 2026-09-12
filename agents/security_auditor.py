"""Security Auditor agent: detects vulnerabilities in Solidity contracts.

Focus areas: reentrancy, integer overflow/underflow, access control,
state management, and unsafe delegatecall usage.
"""

import json

import anthropic

import config

SYSTEM_PROMPT = """You are a smart contract security auditor. You review Solidity \
code for vulnerabilities and respond with JSON only — no markdown, no preamble, \
no explanation outside the JSON structure.

Focus exclusively on security issues in these categories:
- Reentrancy
- Integer overflow / underflow
- Access control
- State management
- Unsafe delegatecall usage

Do not comment on gas efficiency, code style, or business logic correctness — \
those are handled by other agents.

Respond with a single JSON object matching this exact shape:
{
  "agent": "security_auditor",
  "findings": [
    {
      "type": "reentrancy | overflow | access_control | state_management | delegatecall",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "location": "function or line reference",
      "description": "what the vulnerability is",
      "exploitation_scenario": "how an attacker could exploit this",
      "recommended_fix": "concrete fix"
    }
  ]
}

If no issues are found, return {"agent": "security_auditor", "findings": []}."""


def analyze(contract_code: str) -> dict:
    """Run the security auditor agent against Solidity source and return parsed JSON findings."""
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
            "agent": "security_auditor",
            "findings": [],
            "error": f"Failed to parse agent response as JSON: {exc}",
            "raw_response": raw_text,
        }
