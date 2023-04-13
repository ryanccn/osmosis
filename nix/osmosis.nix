{
  lib,
  stdenv,
  aipython3,
  coremltools,
  fetchFromGitHub,
  fetchPypi,
  osmosis-frontend,
  version,
  isNvidia ? false,
  ...
}: let
  inherit (lib) cleanSource licenses maintainers;
  inherit (aipython3) buildPythonPackage;

  # for some reason this doesn't build by default...
  compel = aipython3.compel.overridePythonAttrs (_: rec {
    pname = "compel";
    version = "1.0.5";

    src = fetchPypi {
      inherit pname version;
      sha256 = "sha256-vpMXDsB+7t+ZxlSt795jsBZ76ZqbQlTe0XhAuA/LfFI=";
    };

    propagatedBuildInputs = with aipython3; [
      setuptools
      diffusers
      pyparsing
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
    version = "5.3.3";
    src = fetchFromGitHub {
      owner = "miguelgrinberg";
      repo = "Flask-SocketIO";
      rev = "v${version}";
      sha256 = "sha256-oqy6tSk569QaSkeNsyXuaD6uUB3yuEFg9Jwh5rneyOE=";
    };

    checkInputs = with aipython3; [
      coverage
      pytestCheckHook
      redis
    ];
  });

  omegaconf = aipython3.omegaconf.overridePythonAttrs (_: rec {
    # this fails because of a deprecation warning, not anything serious
    doCheck = false;
  });

  pyre-extensions = buildPythonPackage rec {
    pname = "pyre-extensions";
    version = "0.0.23";
    format = "wheel";
    src = fetchPypi rec {
      pname = "pyre_extensions";
      inherit version format;
      sha256 = "sha256-6UX99BExcs7FF8Xa7KVvYfZjL9W42BZfElPIhlyH5is=";
      dist = python;
      python = "py3";
    };

    propagatedBuildInputs = with aipython3; [
      typing-extensions
      typing-inspect
    ];
  };

  # allows for cuda support
  xformers = buildPythonPackage rec {
    pname = "xformers";
    version = "0.0.16";
    format = "wheel";

    src = builtins.fetchurl {
      url = "https://files.pythonhosted.org/packages/b3/90/178f8dec2d3f9b60f4d29954bc2d605ee8e8e762094047fc4ec0b94d13c0/xformers-0.0.16-cp310-cp310-manylinux2014_x86_64.whl";
      sha256 = "sha256:03kgf90zz3kfz05zx9sm0cr5xwzlgp6qhr4qyfz9ddjq69k7fjm6";
    };

    propagatedBuildInputs = with aipython3; [
      torch
      numpy
      pyre-extensions
    ];

    doCheck = false;
  };
in
  buildPythonPackage {
    pname = "osmosis";
    inherit version;

    format = "flit";
    src = cleanSource ./..;

    propagatedBuildInputs = with aipython3;
      [
        accelerate
        click
        compel
        diffusers
        eventlet
        flask
        flask-socketio
        flit-core
        gfpgan
        psutil
        omegaconf
        realesrgan
        rich
        safetensors
        torch
        transformers
        tqdm
      ]
      ++ (
        if isNvidia
        then [xformers]
        else []
      )
      ++ (
        if stdenv.isDarwin
        then [coremltools]
        else []
      );

    # thanks https://nixified.ai/!
    makeWrapperArgs = [
      ''        --run '
                if [ -d "/usr/lib/wsl/lib" ]
                then
                  echo "Running via WSL (Windows Subsystem for Linux), setting LD_LIBRARY_PATH=/usr/lib/wsl/lib"
                	set -x
                	export LD_LIBRARY_PATH="/usr/lib/wsl/lib"
                	set -x
                fi
                '
      ''
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
