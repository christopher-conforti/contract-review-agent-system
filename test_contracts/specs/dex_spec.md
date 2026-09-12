# Minimal AMM Swap Specification

Applies to: `test_contracts/uniswap_snippet.sol`

## Required State

- `reserve0`, `reserve1`: the pool's reserves of token0 and token1, set at
  construction and updated on every swap.

## Required Behavior

1. **`swap0For1(amountIn)`**
   - MUST revert if `amountIn` is zero.
   - MUST compute `amountOut` using the constant-product formula:
     `amountOut = (amountIn * reserve1) / (reserve0 + amountIn)`.
   - MUST increase `reserve0` by `amountIn` and decrease `reserve1` by
     `amountOut`.
   - MUST emit a `Sync` event with the updated reserves after every swap.
   - MUST accept a caller-supplied minimum acceptable output
     (`minAmountOut`) and revert if the computed `amountOut` is below it, so
     a swapper is protected against price movement between submission and
     execution.
   - MUST NOT allow `reserve1` to be decreased below zero.
2. **`getPrice0()`**
   - MUST revert if `reserve0` is zero.
   - MUST return the price of token0 in terms of token1, scaled by `1e18`.

## Invariants

- The constant-product invariant `reserve0 * reserve1` must not decrease as a
  result of any swap (ignoring intentional fee deduction, which this
  specification does not require).
- `reserve0` and `reserve1` must never be negative.
