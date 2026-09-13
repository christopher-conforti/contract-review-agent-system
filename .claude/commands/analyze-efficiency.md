Read the Solidity contract at `$ARGUMENTS`, then analyze it for gas inefficiencies. Scope is limited to gas and execution cost — do not comment on security, logic correctness, or code style.

Focus areas:
- **Storage**: unnecessary SLOADs/SSTOREs, variables that could be packed into fewer slots, `storage` vs `memory` pointer misuse
- **Loops**: unbounded iterations, redundant reads inside loops, loop invariants that should be hoisted
- **Data types**: `uint256` where smaller types suffice after packing, `bytes32` vs `string`
- **Calldata**: `memory` params that should be `calldata` in external functions
- **Redundancy**: recomputed values that could be cached, duplicate events, dead code

**Consult the global knowledge base before analyzing:**
Run `ls ~/.claude/knowledge/eips/ ~/.claude/knowledge/solidity/ 2>/dev/null | head -3` to check availability.
If `~/.claude/knowledge/` is empty or absent, auto-populate it first:
```bash
python3 ~/.claude/knowledge/sync.py
```
Then:
- Detect which EIP standard this contract implements (EIP-20: transfer/approve/balanceOf; EIP-721: ownerOf/tokenURI; EIP-1155: safeTransferFrom+id+amount; EIP-4626: deposit/withdraw/convertToShares; EIP-1967: delegatecall+fixed slot). Read `~/.claude/knowledge/eips/eip-{N}.md` for detected standards — use it to confirm which behaviors are mandated and cannot be optimized away.
- Read `~/.claude/knowledge/solidity/units-and-global-variables.rst` for opcode gas costs.

Also try running `slither $ARGUMENTS --print variables-order,function-summary` via Bash to surface storage layout and visibility info. If slither is unavailable, proceed without it.

Format your response as:

## Gas Efficiency Analysis: `<filename>`

For each finding:

### [HIGH|MEDIUM|LOW] — <short title>
| Field | Detail |
|---|---|
| **Category** | storage \| loops \| data_types \| calldata \| redundancy |
| **Location** | function or line reference |
| **Issue** | what costs extra gas and why |
| **Estimated impact** | rough gas savings if known |
| **Fix** | concrete change |

End with:

---
**Summary**: X HIGH · Y MEDIUM · Z LOW impact findings
