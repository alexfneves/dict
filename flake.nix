{
  inputs = {
    nixpkgs.url = "github:cachix/devenv-nixpkgs/rolling";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    devenv.inputs.nixpkgs.follows = "nixpkgs";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs =
    {
      self,
      nixpkgs,
      devenv,
      systems,
      ...
    }@inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      packages = forEachSystem (system: {
        devenv-up = self.devShells.${system}.default.config.procfileScript;
        devenv-test = self.devShells.${system}.default.config.test;
      });

      devShells = forEachSystem (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = devenv.lib.mkShell {
            inherit inputs pkgs;
            modules = [
              {
                # https://devenv.sh/reference/options/
                packages = [
                  pkgs.cmake
                  pkgs.clang-tools
                  pkgs.ftxui
                  pkgs.inotify-tools
                ];

                git-hooks.excludes = [ ".devenv" ];
                git-hooks.hooks = {
                  clang-format.enable = true;
                  clang-tidy.enable = true;
                  # cmake-format.enable = true;
                  nixfmt-rfc-style.enable = true;
                };

                enterShell = ''
                  echo "Dict dev shell"
                '';

                scripts.build.exec = ''
                  cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
                  cmake --build build
                '';
                scripts.dict.exec = ''
                  ./build/dict
                '';

                scripts.dict-reload.exec = ''
                  bash scripts/dict-reload;
                '';
              }
            ];
          };
        }
      );
    };
}
