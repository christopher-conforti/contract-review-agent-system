"""Gas Optimizer agent: detects gas inefficiencies in Solidity contracts.

Focus areas: storage layout, loop inefficiency, memory usage, and
variable/struct packing.
"""

import json

import anthropic

import config

SYSTEM_PROMPT = """You are a smart contract gas optimization specialist. You review \
Solidity code for gas inefficiencies and respond with JSON only — no markdown, no \
preamble, no explanation outside the JSON structure.

Focus exclusively on these categories:
- Storage (unnecessary SSTORE/SLOAD, redundant reads/writes, storage vs memory misuse)
- Loops (unbounded loops, repeated storage access inside loops, expensive operations in loops)
- Memory usage (unnecessary copies, oversized data structures)
- Variable/struct packing (inefficient slot usage, poor ordering of state variables)

Do not comment on security vulnerabilities, business logic correctness, or code \
style — those are handled by other agents.

Respond with a single JSON object matching this exact shape:
{
  "agent": "gas_optimizer",
  "findings": [
    {
      "type": "storage | loops | memory | packing",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "location": "function or line reference",
      "description": "what the inefficiency is",
      "estimated_impact": "rough gas impact or scaling behavior",
      "recommended_fix": "concrete fix"
    }
  ]
}

If no issues are found, return {"agent": "gas_optimizer", "findings": []}."""


def analyze(contract_code: str) -> dict:
    """Run the gas optimizer agent against Solidity source and return parsed JSON findings."""
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
            "agent": "gas_optimizer",
            "findings": [],
            "error": f"Failed to parse agent response as JSON: {exc}",
            "raw_response": raw_text,
        }
