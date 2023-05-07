_: {
  imports = [
    ./flake
    ./packages
  ];

  # systems to declare packages for
  systems = [
    "x86_64-linux"
    "x86_64-darwin"
    "aarch64-darwin"
  ];
}
