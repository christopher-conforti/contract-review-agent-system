"""Spec Compliance agent: validates a Solidity contract against a formal spec.

Optional agent — only runs when a specification document is supplied alongside
the contract. Checks that the contract's behavior matches what the spec requires.
"""

import json

import anthropic

import config

SYSTEM_PROMPT = """You are a smart contract specification compliance reviewer. You \
are given Solidity contract code and a formal specification document, and you \
check whether the contract's behavior satisfies the spec. Respond with JSON only \
— no markdown, no preamble, no explanation outside the JSON structure.

Focus exclusively on whether the contract implements what the spec requires:
- Missing functionality the spec requires
- Behavior that contradicts the spec
- Ambiguous areas where the contract's behavior cannot be verified against the spec

Do not comment on security vulnerabilities, gas efficiency, or general code \
quality — those are handled by other agents. Only flag deviations from the \
supplied spec.

The input will contain two sections: "SPEC:" followed by the specification, then \
"CONTRACT:" followed by the Solidity source.

Respond with a single JSON object matching this exact shape:
{
  "agent": "spec_compliance",
  "findings": [
    {
      "type": "missing_functionality | contradicts_spec | ambiguous",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "spec_reference": "the relevant spec section or requirement",
      "location": "function or line reference in the contract, if applicable",
      "description": "how the contract deviates from the spec",
      "recommended_fix": "concrete fix"
    }
  ]
}

If the contract fully complies with the spec, return {"agent": "spec_compliance", "findings": []}."""


def analyze(contract_code: str, spec: str) -> dict:
    """Run the spec compliance agent against Solidity source and a spec, return parsed JSON findings."""
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    user_content = f"SPEC:\n{spec}\n\nCONTRACT:\n{contract_code}"

    response = client.messages.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )

    raw_text = response.content[0].text

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        return {
            "agent": "spec_compliance",
            "findings": [],
            "error": f"Failed to parse agent response as JSON: {exc}",
            "raw_response": raw_text,
        }
