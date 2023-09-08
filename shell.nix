{ pkgs ? import <nixpkgs> { config.allowUnfree = true; } }:
with pkgs;
mkShell {

  # nativeBuildInputs is usually what you want -- tools you need to run
  nativeBuildInputs = [
    rshell
    (python3.withPackages (ps: with python3Packages; [
      #ipython
      python-lsp-server
      #pyftdi
    ]))
    libusb1
    usbutils # lsusb
    p7zip
  ];
}
