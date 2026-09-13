Read the Solidity contract at `$ARGUMENTS`, then validate its logic and algorithmic correctness. Do not comment on gas efficiency, code style, or security vulnerabilities — those are handled elsewhere.

Focus areas:
- **Algorithm correctness**: does the implementation match the evident intent?
- **Edge cases**: zero values, max values, empty inputs, single-element collections
- **Invariants**: are expected invariants (e.g. total supply = sum of balances) maintained across all code paths?
- **Rounding and precision**: integer division truncation, fee calculation errors, off-by-one
- **State machine**: are all state transitions valid? Are invalid transitions blocked?
- **Preconditions**: are inputs validated before use?

**Consult the knowledge base before analyzing:**
Run `ls knowledge/eips/ knowledge/solidity/ 2>/dev/null` to check availability.
- Detect which EIP standard this contract implements (EIP-20: transfer/approve/balanceOf; EIP-721: ownerOf/tokenURI; EIP-1155: safeTransferFrom+id+amount; EIP-4626: deposit/withdraw/convertToShares; EIP-1967: delegatecall+fixed slot). Read `knowledge/eips/eip-{N}.md` for detected standards — the EIP is the authoritative definition of correct logic; deviations are findings.
- If `knowledge/solidity/known-bugs.json` exists, read it and cross-check for compiler bugs that affect the contract's pragma version and could cause incorrect logic.
- If `knowledge/` is absent or empty, note it and proceed — run `/sync-knowledge` to populate.

Try running `solc --ast-compact-json $ARGUMENTS 2>&1` via Bash to check for compilation errors that reveal logic issues. If solc is unavailable, proceed without it.

Format your response as:

## Logic Validation: `<filename>`

For each finding:

### [CRITICAL|HIGH|MEDIUM|LOW] — <short title>
| Field | Detail |
|---|---|
| **Category** | algorithm \| edge_case \| invariant \| rounding \| state_machine \| precondition |
| **EIP reference** | cited section if the finding relates to a standard (if knowledge base is populated) |
| **Location** | function or line reference |
| **Issue** | what the logic bug is |
| **Impact** | what goes wrong at runtime |
| **Fix** | concrete correction |

End with:

---
**Summary**: X CRITICAL · Y HIGH · Z MEDIUM · W LOW
