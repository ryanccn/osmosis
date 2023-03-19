{
  lib,
  #stdenv, this is for future darwin support
  aipython3,
  fetchFromGitHub,
  fetchPypi,
  osmosis-frontend,
  python3Packages,
  version,
  ...
}: let
  inherit (lib) cleanSource licenses maintainers;
  inherit (python3Packages) buildPythonPackage;

  # for some reason this doesn't build by default...
  compel = aipython3.compel.overridePythonAttrs (_: {
    propagatedBuildInputs = with aipython3; [
      setuptools
      diffusers
      python3Packages.pyparsing
      transformers
      torch
    ];
  });

  accelerate = aipython3.accelerate.overridePythonAttrs (_: rec {
    version = "0.17.1";
    src = fetchPypi {
      pname = "accelerate";
      inherit version;
      sha256 = "sha256-+K024c4YaWC7l1vRYn3LCWLCBGZY0+wWF1g+vcWY9Zk=";
    };
  });

  # pyproject.toml requires ~= 5.3.2
  # TODO: remove this when it gets updated in nixpkgs
  flask-socketio = aipython3.flask-socketio.overridePythonAttrs (_: rec {
    version = "5.3.2";
    src = fetchFromGitHub {
      owner = "miguelgrinberg";
      repo = "Flask-SocketIO";
      rev = "v${version}";
      sha256 = "sha256-fjHNvabuznhSK12uiYReQam9j2zvAsMrjW2f3TFtL24=";
    };

    checkInputs = with aipython3; [
      coverage
      pytestCheckHook
      redis
    ];
  });
in
  buildPythonPackage {
    pname = "osmosis";
    inherit version;

    format = "flit";
    src = cleanSource ./..;

    propagatedBuildInputs = with aipython3; [
      accelerate
      click
      compel
      # TODO: install this for darwin
      #coremltools
      diffusers
      eventlet
      flask
      flask-socketio
      flit-core
      gfpgan
      realesrgan
      rich
      torch
      transformers
      tqdm
    ];

    # possible TODO: there might be a
    # better way to do this...
    patchPhase = ''
      frontend_dir="osmosis/frontend/"
      dist_dir="libexec/frontend/deps/frontend/dist"

      cp -r ${osmosis-frontend}/"$dist_dir" "$frontend_dir"/
    '';

    meta = {
      homepage = "https://github.com/ryanccn/osmosis";
      description = "An experimental Stable Diffusion frontend";
      license = with licenses; [agpl3Plus];
      maintainers = with maintainers; [getchoo];
    };
  }
