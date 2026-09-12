"""Orchestrator: runs all review agents against a contract and consolidates findings.

Usage:
    python orchestrator.py --contract path/to/contract.sol [--spec path/to/spec.md]
"""

import argparse
import json
import os
from datetime import datetime, timezone

from agents import (
    best_practices,
    gas_optimizer,
    logic_validator,
    security_auditor,
    spec_compliance,
)

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def run_agents(contract_code: str, spec: str | None) -> list[dict]:
    """Run every agent sequentially and return their raw results in order."""
    results = [
        security_auditor.analyze(contract_code),
        gas_optimizer.analyze(contract_code),
        logic_validator.analyze(contract_code),
        best_practices.analyze(contract_code),
    ]

    if spec:
        results.append(spec_compliance.analyze(contract_code, spec))

    return results


def consolidate(agent_results: list[dict]) -> dict:
    """Merge per-agent results into one report, tagging each finding with its source agent."""
    findings = []

    for result in agent_results:
        agent_name = result.get("agent", "unknown")
        for finding in result.get("findings", []):
            findings.append({"agent": agent_name, **finding})
        if "error" in result:
            findings.append(
                {
                    "agent": agent_name,
                    "type": "agent_error",
                    "severity": "LOW",
                    "description": result["error"],
                }
            )

    findings.sort(key=lambda f: SEVERITY_ORDER.get(f.get("severity"), len(SEVERITY_ORDER)))

    counts = {level: 0 for level in SEVERITY_ORDER}
    for finding in findings:
        severity = finding.get("severity")
        if severity in counts:
            counts[severity] += 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": counts,
        "requires_human_review": counts["CRITICAL"] > 0 or counts["HIGH"] > 0,
        "findings": findings,
    }


def write_report(report: dict, contract_path: str) -> str:
    """Write the consolidated report to reports/ and return the output path."""
    os.makedirs("reports", exist_ok=True)
    contract_name = os.path.splitext(os.path.basename(contract_path))[0]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = os.path.join("reports", f"{contract_name}_{timestamp}.json")

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Run the contract review agent pipeline.")
    parser.add_argument("--contract", required=True, help="Path to the Solidity contract file.")
    parser.add_argument("--spec", help="Optional path to a specification document.")
    args = parser.parse_args()

    with open(args.contract) as f:
        contract_code = f.read()

    spec = None
    if args.spec:
        with open(args.spec) as f:
            spec = f.read()

    agent_results = run_agents(contract_code, spec)
    report = consolidate(agent_results)
    output_path = write_report(report, args.contract)

    print(f"Report written to {output_path}")
    print(f"Findings by severity: {report['summary']}")
    if report["requires_human_review"]:
        print("CRITICAL or HIGH severity findings present — human review required before proceeding.")


if __name__ == "__main__":
    main()
