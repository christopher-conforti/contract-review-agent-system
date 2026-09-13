{
  description = "Solidity contract review via Claude Code skills";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.python3            # knowledge/sync.py (stdlib only)
            pkgs.foundry            # forge, cast, anvil, chisel
            pkgs.solc               # Solidity compiler
            pkgs.slither-analyzer   # static analysis
          ];
          shellHook = ''
            echo "contract-review dev shell"
            echo "  /sync-knowledge          populate ~/.claude/knowledge/ from EIPs, SWC, Solidity docs"
            echo "  /orchestrate-solidity-review <contract> [spec]"
            echo "  forge build / forge test / anvil"
            echo "  slither <contract.sol>"
          '';
        };
      }
    );
}
