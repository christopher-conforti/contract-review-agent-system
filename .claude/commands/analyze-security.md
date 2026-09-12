Read the Solidity contract at `$ARGUMENTS`, then perform a security audit scoped exclusively to these categories — do not comment on gas, style, or business logic:

- **Reentrancy**: external calls before state updates, missing reentrancy guards
- **Integer overflow/underflow**: unchecked arithmetic, pre-0.8.0 SafeMath absence
- **Access control**: missing role guards, `tx.origin` auth, unprotected initializers
- **State management**: checks-effects-interactions violations, storage ordering bugs
- **Delegatecall**: unsafe proxy patterns, storage slot collisions

Also try running `slither $ARGUMENTS` via Bash. If slither is unavailable or errors, proceed without it. Incorporate any slither findings that fall within the above categories; ignore findings outside scope.

Format your response as:

## Security Audit: `<filename>`

For each finding:

### [CRITICAL|HIGH|MEDIUM|LOW] — <short title>
| Field | Detail |
|---|---|
| **Type** | reentrancy \| overflow \| access_control \| state_management \| delegatecall |
| **Location** | function or line reference |
| **Description** | what the vulnerability is |
| **Exploitation** | how an attacker exploits it |
| **Fix** | concrete remediation |

End with:

---
**Summary**: X CRITICAL · Y HIGH · Z MEDIUM · W LOW
