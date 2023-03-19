{
  pkgs,
  lib,
  version,
  nixified-ai,
}: let
  inherit (pkgs) callPackage;

  aipython3 = (import "${nixified-ai}/modules/aipython3" {inherit lib;}).perSystem {inherit pkgs;};
  inherit (aipython3.dependencySets) aipython3-amd aipython3-nvidia;

  mkOsmosis = args: callPackage ./osmosis.nix ({inherit version;} // args);
in {
  packages = rec {
    osmosis-frontend = callPackage ./osmosis-frontend.nix {};
    osmosis-nvidia = mkOsmosis {
      aipython3 = aipython3-nvidia;
      inherit osmosis-frontend;
    };
    osmosis-amd = mkOsmosis {
      aipython3 = aipython3-amd;
      inherit osmosis-frontend;
    };
  };
}
