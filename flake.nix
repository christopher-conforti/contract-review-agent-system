{
  description = "Multi-agent smart contract review system";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python3.withPackages (ps: [ ps.anthropic ]);
      in {
        packages.default = pkgs.writeShellApplication {
          name = "contract-review";
          runtimeInputs = [ pythonEnv ];
          text = ''
            exec python "${self}/orchestrator.py" "$@"
          '';
        };

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/contract-review";
        };

        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv ];
          shellHook = ''
            echo "contract-review dev shell — run: python orchestrator.py --contract <path>"
          '';
        };
      }
    );
}
