Read the Solidity contract at `$ARGUMENTS`, then review it for adherence to Solidity best practices and code quality. Do not comment on security vulnerabilities, gas costs, or business logic correctness.

Focus areas:
- **Naming**: do variables, functions, events, and errors follow Solidity conventions (camelCase functions, PascalCase contracts/events, UPPER_SNAKE constants)?
- **Error handling**: `require` with descriptive messages, custom errors (preferred over string revert), `assert` used only for invariants
- **Events**: are all important state changes emitted? Are indexed fields chosen correctly?
- **Documentation**: NatSpec on public/external functions? Parameter docs?
- **Code organization**: visibility specifiers present on all functions/state vars, `immutable` and `constant` used where applicable, function ordering (constructor → external → public → internal → private)
- **Compiler hygiene**: pragma pinned or reasonably bounded, no deprecated syntax, no floating pragma

**Consult the global knowledge base before analyzing:**
Run `ls ~/.claude/knowledge/eips/ ~/.claude/knowledge/solidity/ 2>/dev/null | head -3` to check availability.
If `~/.claude/knowledge/` is empty or absent, auto-populate it first:
```bash
python3 ~/.claude/knowledge/sync.py
```
Then:
- Detect which EIP standard this contract implements (EIP-20: transfer/approve/balanceOf; EIP-721: ownerOf/tokenURI; EIP-1155: safeTransferFrom+id+amount; EIP-4626: deposit/withdraw/convertToShares). Read `~/.claude/knowledge/eips/eip-{N}.md` for detected standards — EIPs often mandate specific event signatures, error conditions, and return values that constitute required practices for compliant implementations.
- Read `~/.claude/knowledge/solidity/common-patterns.rst` as the reference for idiomatic Solidity patterns.

Try running `slither $ARGUMENTS --print contract-summary` via Bash for a structural overview. If unavailable, proceed without it.

Format your response as:

## Best Practices Review: `<filename>`

For each finding:

### [HIGH|MEDIUM|LOW|INFO] — <short title>
| Field | Detail |
|---|---|
| **Category** | naming \| error_handling \| events \| documentation \| organization \| compiler |
| **EIP reference** | cited section if the finding relates to a standard requirement (if knowledge base is populated) |
| **Location** | function, variable, or line reference |
| **Issue** | what convention is violated or missing |
| **Fix** | concrete improvement |

End with:

---
**Summary**: X HIGH · Y MEDIUM · Z LOW · W INFO
