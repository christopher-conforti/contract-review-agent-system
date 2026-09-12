Arguments: `<contract_path> <spec_path>`

Parse `$ARGUMENTS` to extract the contract path (first token) and specification path (second token). Read both files.

Before analyzing, detect which EIP standards the contract likely implements by scanning for characteristic identifiers:
- EIP-20: `transfer`, `approve`, `transferFrom`, `balanceOf`, `allowance` → EIP number 20
- EIP-721: `ownerOf`, `safeTransferFrom`, `tokenURI`, `getApproved` → EIP number 721
- EIP-1155: `safeTransferFrom` with `uint256 id` and `uint256 amount` → EIP number 1155
- EIP-4626: `deposit`, `withdraw`, `convertToShares`, `convertToAssets` → EIP number 4626
- EIP-1967: `delegatecall` with fixed storage slots → EIP number 1967

For each detected EIP, lazy-fetch and cache the authoritative spec via Bash:
```bash
EIP=<number>
CACHE="eip_cache/eip-${EIP}.md"
[ -f "$CACHE" ] || curl -sf "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-${EIP}.md" -o "$CACHE"
cat "$CACHE"
```
Use the cached EIP text as a supplementary reference alongside the supplied spec. If fetching fails, proceed without it.

Then validate whether the contract's behavior satisfies the specification.

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
