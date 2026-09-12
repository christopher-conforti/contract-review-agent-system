Read the Solidity contract at `$ARGUMENTS`, then review it for adherence to Solidity best practices and code quality. Do not comment on security vulnerabilities, gas costs, or business logic correctness.

Focus areas:
- **Naming**: do variables, functions, events, and errors follow Solidity conventions (camelCase functions, PascalCase contracts/events, UPPER_SNAKE constants)?
- **Error handling**: `require` with descriptive messages, custom errors (preferred over string revert), `assert` used only for invariants
- **Events**: are all important state changes emitted? Are indexed fields chosen correctly?
- **Documentation**: NatSpec on public/external functions? Parameter docs?
- **Code organization**: visibility specifiers present on all functions/state vars, `immutable` and `constant` used where applicable, function ordering (constructor → external → public → internal → private)
- **Compiler hygiene**: pragma pinned or reasonably bounded, no deprecated syntax, no floating pragma

Try running `slither $ARGUMENTS --print contract-summary` via Bash for a structural overview. If unavailable, proceed without it.

Format your response as:

## Best Practices Review: `<filename>`

For each finding:

### [HIGH|MEDIUM|LOW|INFO] — <short title>
| Field | Detail |
|---|---|
| **Category** | naming \| error_handling \| events \| documentation \| organization \| compiler |
| **Location** | function, variable, or line reference |
| **Issue** | what convention is violated or missing |
| **Fix** | concrete improvement |

End with:

---
**Summary**: X HIGH · Y MEDIUM · Z LOW · W INFO
