# file for declaring misc flake options,
# mainly for development
{
  inputs,
  self,
  ...
}: {
  flake = {
    # call our packages module manually to export our packages
    overlays.default = final: _: let
      packages = import ../packages {inherit inputs self;};
    in
      (packages.perSystem {pkgs = final;}).packages;
  };

  perSystem = {
    pkgs,
    system,
    ...
  }: {
    checks = {
      pre-commit-check = inputs.pre-commit-hooks.lib.${system}.run {
        src = ./.;
        hooks = {
          alejandra.enable = true;
          black.enable = true;
          deadnix.enable = true;
          prettier.enable = true;
          statix.enable = true;
        };
      };
    };

    devShells = let
      inherit (pkgs) mkShell alejandra deadnix nodePackages nodejs python39 statix yarn;
      inherit (self.checks.${system}.pre-commit-check) shellHook;
    in {
      default = mkShell {
        inherit shellHook;
        packages = with nodePackages;
          [
            alejandra
            deadnix
            eslint
            nodejs
            prettier
            statix
            yarn
          ]
          ++ [(python39.withPackages (p: with p; [black]))];
      };
    };

    formatter = pkgs.alejandra;
  };
}
