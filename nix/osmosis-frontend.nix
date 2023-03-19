{
  lib,
  mkYarnPackage,
  ...
}:
mkYarnPackage rec {
  name = "osmosis-frontend";
  src = lib.cleanSource ../osmosis/frontend;
  packageJSON = src + "/package.json";
  yarnLock = src + "/yarn.lock";
  buildPhase = ''
    export HOME="$(mktemp -d)"
    yarn --offline build
  '';
}
