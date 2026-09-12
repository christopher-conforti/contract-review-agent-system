// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title GasInefficientRegistry
/// @notice Intentionally gas-inefficient contract for testing the gas optimizer agent.
/// Contains repeated storage reads inside a loop, poor struct packing, and an
/// unbounded loop over a dynamically growing array.
contract GasInefficientRegistry {
    struct Entry {
        uint256 id;
        bool active;
        uint256 createdAt;
        address owner;
    }

    Entry[] public entries;
    uint256 public totalActive;

    function addEntry(address owner) external {
        entries.push(Entry({
            id: entries.length,
            active: true,
            createdAt: block.timestamp,
            owner: owner
        }));
        totalActive += 1;
    }

    /// @dev Reads entries.length from storage on every loop iteration instead
    /// of caching it once, and reads/writes totalActive per-entry instead of
    /// accumulating in memory.
    function deactivateAll() external {
        for (uint256 i = 0; i < entries.length; i++) {
            if (entries[i].active) {
                entries[i].active = false;
                totalActive -= 1;
            }
        }
    }

    /// @dev Unbounded loop over the full entries array — gas cost grows without
    /// bound as more entries are added, risking a block gas limit failure.
    function countActiveForOwner(address owner) external view returns (uint256 count) {
        for (uint256 i = 0; i < entries.length; i++) {
            if (entries[i].owner == owner && entries[i].active) {
                count++;
            }
        }
    }
}
