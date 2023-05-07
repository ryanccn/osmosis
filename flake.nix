{
  description = "An experimental Stable Diffusion frontend";

  # this allows us to use nixified-ai's and our own cachix instance
  # so we don't have to rebuild all the time :)
  nixConfig = {
    extra-substituters = [
      "https://ai.cachix.org"
      "https://osmosis.cachix.org"
    ];
    extra-trusted-public-keys = [
      "ai.cachix.org-1:N9dzRK+alWwoKXQlnn0H6aUx0lU/mspIoz8hMvGvbbc="
      "osmosis.cachix.org-1:mq0PbolVaW/p61SJvxfXbq6UkEmkWg6xdLL3uUPrr9g="
    ];
  };

  inputs = {
    nixpkgs.url = "nixpkgs/3c5319ad3aa51551182ac82ea17ab1c6b0f0df89";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
    nixified-ai = {
      url = "github:nixified-ai/flake";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-parts.follows = "flake-parts";
    };
    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-compat.follows = "flake-compat";
    };
  };

  outputs = inputs:
    inputs.flake-parts.lib.mkFlake {inherit inputs;} {imports = [./nix];};
}
