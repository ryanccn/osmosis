{
  python3Packages,
  fetchFromGitHub,
  ...
}: let
  inherit (python3Packages) buildPythonPackage;
in
  buildPythonPackage rec {
    pname = "coremltools";
    version = "6.2";

    src = fetchFromGitHub {
      owner = "apple";
      repo = "coremltools";
      rev = version;
      sha256 = "sha256-t9B60H7nIDCq1aXfXQaofFYYXIQ4MUv+V6S3EcogWz8=";
    };

    doCheck = false;

    propagatedBuildInputs = with python3Packages; [
      numpy
      packaging
      protobuf
      setuptools
      sympy
      tqdm
    ];
  }
