// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title VulnerableVault
/// @notice Intentionally vulnerable contract for testing the security auditor agent.
/// Contains a classic reentrancy bug, a missing access control check, and an
/// unchecked delegatecall. Do not deploy.
contract VulnerableVault {
    mapping(address => uint256) public balances;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    /// @dev Reentrancy: external call happens before the balance is zeroed out,
    /// so a malicious contract's fallback can call withdraw() again before the
    /// state update takes effect.
    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient balance");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "transfer failed");

        balances[msg.sender] -= amount;
    }

    /// @dev Access control: anyone can drain the contract, not just the owner.
    function emergencyWithdraw(uint256 amount) external {
        (bool success, ) = owner.call{value: amount}("");
        require(success, "transfer failed");
    }

    /// @dev Unchecked delegatecall: forwards arbitrary calldata to an
    /// attacker-controlled target with the vault's own storage context.
    function execute(address target, bytes calldata data) external {
        (bool success, ) = target.delegatecall(data);
        require(success, "execution failed");
    }
}
