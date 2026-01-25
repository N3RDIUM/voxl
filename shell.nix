{
  pkgs ? import <nixpkgs> { },
}:

let
  pyfastnoisesimd = import ./deps/pyfastnoisesimd.nix {
    inherit (pkgs) lib fetchPypi;
    buildPythonPackage = pkgs.python314Packages.buildPythonPackage;
    numpy = pkgs.python314Packages.numpy;
  };

  dependency-injector = import ./deps/dependency_injector.nix {
    inherit (pkgs) lib fetchPypi;
    buildPythonPackage = pkgs.python314Packages.buildPythonPackage;
    cython = pkgs.python314Packages.cython;
    setuptools = pkgs.python314Packages.setuptools;
  };
in

with pkgs;

mkShell {
  buildInputs = [
    # Necessary dependencies
    python314
    python314Packages.pyglm
    python314Packages.cython
    python314Packages.numpy
    python314Packages.pillow
    python314Packages.pyzmq
    python314Packages.pyyaml
    python314Packages.wgpu-py

    # Vulkan compute backend
    vulkan-tools           # For vulkaninfo, etc.
    vulkan-loader
    vulkan-validation-layers
    libxkbcommon
    wayland
    xorg.libX11
    xorg.libXcursor
    xorg.libXrandr
    xorg.libXi
    pkg-config

    # glfw window backend
    python314Packages.glfw

    # OpenGL render backend
    python314Packages.pyopengl
    python314Packages.pyopengl-accelerate

    # Development
    ruff
    basedpyright
    nixfmt
    python314Packages.mypy

    # Documentation
    python314Packages.sphinx
    python314Packages.furo
    python314Packages.sphinx-copybutton
    python314Packages.sphinx-sitemap
    python314Packages.sphinx-multiversion # todo configure

    # Outsourced deps (also necessary)
    dependency-injector
    pyfastnoisesimd
  ];

    nativeBuildInputs = [
    pkgs.pkg-config
  ];

  # Needed for dynamic libraries in some cases
  LD_LIBRARY_PATH = with pkgs; lib.makeLibraryPath [
    vulkan-loader
    wayland
    libxkbcommon
    xorg.libX11
    xorg.libXcursor
    xorg.libXrandr
    xorg.libXi
  ];
}
