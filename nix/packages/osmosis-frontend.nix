{mkYarnPackage, ...}:
mkYarnPackage rec {
  name = "osmosis-frontend";

  src = builtins.path {
    path = ../../osmosis/frontend;
    name = "osmosis-frontend";
  };

  packageJSON = src + "/package.json";
  yarnLock = src + "/yarn.lock";

  buildPhase = ''
    export HOME="$(mktemp -d)"
    yarn --offline build
  '';
}
