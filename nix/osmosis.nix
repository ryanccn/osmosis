{
  lib,
  stdenv,
  aipython3,
  coremltools,
  osmosis-frontend,
  version,
  isNvidia ? false,
  ...
}: let
  inherit (lib) cleanSource licenses maintainers;
  inherit (aipython3) buildPythonPackage;
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
