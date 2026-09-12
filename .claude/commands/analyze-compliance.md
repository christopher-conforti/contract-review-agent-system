Arguments: `<contract_path> <spec_path>`

Parse `$ARGUMENTS` to extract the contract path (first token) and specification path (second token). Read both files. Then validate whether the contract's behavior satisfies the specification.

Scope: deviations from the supplied spec only. Do not report security vulnerabilities, gas issues, or general code quality — those are handled by other agents.

Focus areas:
- **Missing functionality**: requirements in the spec that have no implementation
- **Contradictions**: behavior the contract exhibits that the spec explicitly forbids or defines differently
- **Ambiguities**: spec requirements that cannot be verified from the contract code alone (flag these as LOW so reviewers can clarify)

Format your response as:

## Spec Compliance Review: `<contract filename>` vs `<spec filename>`

For each finding:

### [CRITICAL|HIGH|MEDIUM|LOW] — <short title>
| Field | Detail |
|---|---|
| **Type** | missing_functionality \| contradicts_spec \| ambiguous |
| **Spec reference** | the relevant section, requirement ID, or quoted text |
| **Location** | function or line in the contract, if applicable |
| **Issue** | how the contract deviates from or fails to satisfy the spec |
| **Fix** | what needs to change in the contract (or spec, if the spec is ambiguous) |

If the contract fully complies, say so explicitly.

End with:

---
**Summary**: X CRITICAL · Y HIGH · Z MEDIUM · W LOW (W ambiguous)
