{
  description = "An experimental Stable Diffusion frontend";

  # this allows us to use nixified-ai's cachix instance
  # so we don't have to rebuild all the time :)
  nixConfig = {
    extra-substituters = ["https://ai.cachix.org"];
    extra-trusted-public-keys = ["ai.cachix.org-1:N9dzRK+alWwoKXQlnn0H6aUx0lU/mspIoz8hMvGvbbc="];
  };

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
    flake-utils.url = "github:numtide/flake-utils";
    nixified-ai = {
      url = "github:nixified-ai/flake";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-compat.follows = "flake-compat";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    nixified-ai,
    pre-commit-hooks,
    ...
  }: let
    version = builtins.substring 0 8 self.lastModifiedDate;
    inherit (flake-utils.lib) eachDefaultSystem;
  in
    eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
    in {
      checks = {
        pre-commit-check = pre-commit-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            alejandra.enable = true;
            black.enable = true;
            deadnix.enable = true;
            eslint.enable = true;
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

      packages = let
        inherit
          (import ./nix {
            inherit pkgs version nixified-ai;
            inherit (pkgs) lib;
          })
          packages
          ;
      in
        packages // {default = packages.osmosis-nvidia;};
    });
}
