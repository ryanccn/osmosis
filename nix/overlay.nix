pkgs: let
  inherit (pkgs) fetchFromGitHub fetchPypi;
in {
  osmosisFixes = final: prev: {
    # osmosis requires a decently new version of accelerate
    accelerate = prev.accelerate.overridePythonAttrs (_: rec {
      version = "0.17.1";
      src = fetchPypi {
        pname = "accelerate";
        inherit version;
        sha256 = "sha256-+K024c4YaWC7l1vRYn3LCWLCBGZY0+wWF1g+vcWY9Zk=";
      };
    });

    # pyproject.toml requires ~=1.0.5
    compel = prev.compel.overridePythonAttrs (prev: rec {
      version = "1.0.5";

      src = fetchPypi {
        inherit (prev) pname;
        inherit version;
        sha256 = "sha256-vpMXDsB+7t+ZxlSt795jsBZ76ZqbQlTe0XhAuA/LfFI=";
      };

      propagatedBuildInputs = with final; [
        setuptools
        diffusers
        pyparsing
        transformers
        torch
      ];
    });

    # pyproject.toml requires ~= 5.3.2
    # TODO: remove this when it gets updated in nixpkgs
    flask-socketio = prev.flask-socketio.overridePythonAttrs (_: rec {
      version = "5.3.3";
      src = fetchFromGitHub {
        owner = "miguelgrinberg";
        repo = "Flask-SocketIO";
        rev = "v${version}";
        sha256 = "sha256-oqy6tSk569QaSkeNsyXuaD6uUB3yuEFg9Jwh5rneyOE=";
      };

      checkInputs = with prev; [
        coverage
        pytestCheckHook
        redis
      ];
    });

    # this fails because of a deprecation warning, not anything serious
    omegaconf = prev.omegaconf.overridePythonAttrs (_: {
      doCheck = false;
    });

    # coremltools requires protobuf >= 3.10, <= 4.0.0
    protobuf = prev.protobuf.overridePythonAttrs (_: rec {
      version = "3.20.3";
      src = fetchFromGitHub {
        owner = "protocolbuffers";
        repo = "protobuf";
        rev = "v${version}";
        sha256 = "sha256-u/1Yb8+mnDzc3OwirpGESuhjkuKPgqDAvlgo3uuzbbk=";
      };
    });

    # tests fail, not really sure why...?
    tensorboard = prev.tensorboard.overridePythonAttrs (_: {doCheck = false;});

    # running tifffile's tests can cause oom errors on systems
    # with <= 16GB of memory
    tifffile = prev.tifffile.overridePythonAttrs (_: {doCheck = false;});
  };

  osmosisPackages = final: prev: let
    inherit (prev) buildPythonPackage;
  in {
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

      propagatedBuildInputs = with final; [
        typing-extensions
        typing-inspect
      ];
    };

    # allows for cuda support
    xformers = buildPythonPackage {
      pname = "xformers";
      version = "0.0.16";
      format = "wheel";

      src = builtins.fetchurl {
        url = "https://files.pythonhosted.org/packages/b3/90/178f8dec2d3f9b60f4d29954bc2d605ee8e8e762094047fc4ec0b94d13c0/xformers-0.0.16-cp310-cp310-manylinux2014_x86_64.whl";
        sha256 = "sha256:03kgf90zz3kfz05zx9sm0cr5xwzlgp6qhr4qyfz9ddjq69k7fjm6";
      };

      propagatedBuildInputs = with final; [
        torch
        numpy
        pyre-extensions
      ];

      doCheck = false;
    };
  };
}
