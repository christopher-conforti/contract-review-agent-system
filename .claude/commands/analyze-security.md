Read the Solidity contract at `$ARGUMENTS`, then perform a security audit scoped exclusively to these categories — do not comment on gas, style, or business logic:

- **Reentrancy**: external calls before state updates, missing reentrancy guards
- **Integer overflow/underflow**: unchecked arithmetic, pre-0.8.0 SafeMath absence
- **Access control**: missing role guards, `tx.origin` auth, unprotected initializers
- **State management**: checks-effects-interactions violations, storage ordering bugs
- **Delegatecall**: unsafe proxy patterns, storage slot collisions

**Consult the global knowledge base before analyzing:**
Run `ls ~/.claude/knowledge/swc/ ~/.claude/knowledge/solidity/ 2>/dev/null | head -3` to check availability.
If `~/.claude/knowledge/` is empty or absent, auto-populate it first:
```bash
python3 ~/.claude/knowledge/sync.py
```
Then:
- Read `~/.claude/knowledge/swc/README.md` for the SWC weakness index, then read the entries most relevant to the vulnerability types found (e.g. SWC-107 for reentrancy, SWC-101 for overflow, SWC-115 for tx.origin, SWC-112 for delegatecall). Use SWC classifications to label findings.
- Read `~/.claude/knowledge/solidity/security-considerations.rst` as the authoritative source on known Solidity security pitfalls.
- Read `~/.claude/knowledge/solidity/known-bugs.json` and cross-check for compiler bugs relevant to the contract's pragma version.

Also try running `slither $ARGUMENTS` via Bash. If slither is unavailable, proceed without it. Incorporate any slither findings within the above categories.

Format your response as:

## Security Audit: `<filename>`

For each finding:

### [CRITICAL|HIGH|MEDIUM|LOW] — <short title>
| Field | Detail |
|---|---|
| **Type** | reentrancy \| overflow \| access_control \| state_management \| delegatecall |
| **SWC** | SWC-NNN (if knowledge base is populated) |
| **Location** | function or line reference |
| **Description** | what the vulnerability is |
| **Exploitation** | how an attacker exploits it |
| **Fix** | concrete remediation |

End with:

---
**Summary**: X CRITICAL · Y HIGH · Z MEDIUM · W LOW
