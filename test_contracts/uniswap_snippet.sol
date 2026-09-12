// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title MiniSwap
/// @notice Simplified constant-product AMM swap function, modeled loosely on
/// Uniswap V2, for testing the logic validator and spec compliance agents
/// against test_contracts/specs/dex_spec.md. Intentionally omits the slippage
/// protection and fee-on-transfer handling a production AMM would need.
contract MiniSwap {
    uint256 public reserve0;
    uint256 public reserve1;

    event Sync(uint256 reserve0, uint256 reserve1);

    constructor(uint256 _reserve0, uint256 _reserve1) {
        reserve0 = _reserve0;
        reserve1 = _reserve1;
    }

    /// @dev Constant-product swap: amountOut = (amountIn * reserveOut) / (reserveIn + amountIn).
    /// No minimum-output check, so a swapper has no protection against a price
    /// move (or front-run) between submitting the transaction and it executing.
    function swap0For1(uint256 amountIn) external returns (uint256 amountOut) {
        require(amountIn > 0, "amountIn must be positive");

        amountOut = (amountIn * reserve1) / (reserve0 + amountIn);

        reserve0 += amountIn;
        reserve1 -= amountOut;

        emit Sync(reserve0, reserve1);
    }

    function getPrice0() external view returns (uint256) {
        require(reserve0 > 0, "no liquidity");
        return (reserve1 * 1e18) / reserve0;
    }
}
