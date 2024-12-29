{
  inputs = {
    nixpkgs.url = "github:cachix/devenv-nixpkgs/rolling";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    devenv.inputs.nixpkgs.follows = "nixpkgs";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
    nixpkgs-python.inputs = { nixpkgs.follows = "nixpkgs"; };
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = { self, nixpkgs, devenv, systems, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      packages = forEachSystem (system: {
        devenv-up = self.devShells.${system}.default.config.procfileScript;
        devenv-test = self.devShells.${system}.default.config.test;
      });

      devShells = forEachSystem
        (system:
          let
            pkgs = nixpkgs.legacyPackages.${system};
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  # https://devenv.sh/reference/options/
                  packages = (with pkgs; [
                    python3
                    sqlitebrowser
                  ]) ++ (with pkgs.python311Packages; [
                    mypy
                    debugpy
                    python-lsp-server
                    pylsp-mypy
                    sqlmodel # pre commit mypy and linter mypy would fail without it
                  ]);

                  languages.python = {
                    enable = true;
                    version = "3.11.8";
                    venv = {
                      enable = true;
                      quiet = true;
                    };
                    poetry.enable = true;
                  };

                  pre-commit.hooks = {
                    isort = {
                      enable = true;
                      settings.profile = "black";
                    };
                    black.enable = true;
                    mypy.enable = true;
                  };

                  enterShell = ''
                    echo "Entering dev shell of project dict"
                  '';

                  scripts = {
                    dict.exec = ''
                      poetry run dict "$@";
                    '';
                    dict-dev.exec = ''
                      textual run --dev "dict/main.py $@";
                    '';
                  };
                }
              ];
            };
          });
    };
}
