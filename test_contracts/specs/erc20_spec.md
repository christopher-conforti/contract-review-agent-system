# ERC20 Token Specification

Applies to: `test_contracts/simple_erc20.sol`

## Required State

- `name`, `symbol`: human-readable token identifiers, set once at deployment.
- `decimals`: fixed at 18.
- `totalSupply`: total number of tokens in existence; must equal the sum of all
  account balances at all times.
- `balanceOf[account]`: number of tokens held by `account`.
- `allowance[owner][spender]`: number of tokens `spender` is permitted to
  transfer on `owner`'s behalf.

## Required Behavior

1. **Constructor** must mint the entire `_initialSupply` to the deployer and
   emit a `Transfer` event from the zero address to the deployer.
2. **`transfer(to, amount)`**
   - MUST revert if `to` is the zero address.
   - MUST revert if the caller's balance is less than `amount`.
   - MUST decrease the caller's balance by `amount` and increase `to`'s
     balance by `amount`.
   - MUST emit `Transfer(caller, to, amount)`.
   - MUST return `true` on success.
3. **`approve(spender, amount)`**
   - MUST set `allowance[caller][spender]` to exactly `amount` (overwriting,
     not adding to, any previous allowance).
   - MUST emit `Approval(caller, spender, amount)`.
   - MUST return `true` on success.
4. **`transferFrom(from, to, amount)`**
   - MUST revert if `to` is the zero address.
   - MUST revert if `from`'s balance is less than `amount`.
   - MUST revert if the caller's allowance from `from` is less than `amount`.
   - MUST decrease the caller's allowance from `from` by `amount`.
   - MUST decrease `from`'s balance by `amount` and increase `to`'s balance by
     `amount`.
   - MUST emit `Transfer(from, to, amount)`.
   - MUST return `true` on success.

## Invariants

- `totalSupply` is constant after deployment (no mint/burn functions exist).
- The sum of all `balanceOf` values always equals `totalSupply`.
- No transfer function may ever increase the total token supply.
