{
  pkgs ? import <nixpkgs> { },
}:

let
  pyfastnoisesimd = import ./deps/pyfastnoisesimd.nix {
    inherit (pkgs) lib fetchPypi;
    buildPythonPackage = pkgs.python312Packages.buildPythonPackage;
    numpy = pkgs.python312Packages.numpy;
  };

  dependency-injector = import ./deps/dependency_injector.nix {
    inherit (pkgs) lib fetchPypi;
    buildPythonPackage = pkgs.python312Packages.buildPythonPackage;
    cython = pkgs.python312Packages.cython;
    setuptools = pkgs.python312Packages.setuptools;
    typingextensions = pkgs.python312Packages.typing-extensions;
  };

  imgui = import ./deps/imgui.nix {
    inherit (pkgs) lib fetchPypi;
    buildPythonPackage = pkgs.python312Packages.buildPythonPackage;
    setuptools = pkgs.python312Packages.setuptools;
    wheel = pkgs.python312Packages.wheel;
    cython = pkgs.python312Packages.cython_0;
    python3Packages = pkgs.python312Packages;
  };
in

with pkgs;

mkShell {
  buildInputs = [
    # Necessary dependencies
    python312
    python312Packages.pyglm
    python312Packages.cython
    python312Packages.numpy
    python312Packages.pillow
    python312Packages.pyzmq
    python312Packages.pyyaml
    python312Packages.wgpu-py

    # Vulkan compute backend
    vulkan-tools # For vulkaninfo, etc.
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
    python312Packages.glfw

    # OpenGL render backend
    python312Packages.pyopengl
    python312Packages.pyopengl-accelerate

    # Development
    ruff
    basedpyright
    nixfmt
    python312Packages.mypy

    # Documentation
    python312Packages.sphinx
    python312Packages.furo
    python312Packages.sphinx-copybutton
    python312Packages.sphinx-sitemap
    python312Packages.sphinx-multiversion # todo configure

    # Outsourced deps (also necessary)
    dependency-injector
    pyfastnoisesimd
    imgui
  ];

  nativeBuildInputs = [
    pkgs.pkg-config
  ];

  # Needed for dynamic libraries in some cases
  LD_LIBRARY_PATH =
    with pkgs;
    lib.makeLibraryPath [
      vulkan-loader
      wayland
      libxkbcommon
      xorg.libX11
      xorg.libXcursor
      xorg.libXrandr
      xorg.libXi
    ];
}
