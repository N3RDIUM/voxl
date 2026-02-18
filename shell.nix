{
  pkgs ? import <nixpkgs> { },
}:

let
    pyfastnoisesimd = pkgs.python314.pkgs.callPackage ./deps/pyfastnoisesimd.nix { };
    dependency-injector = pkgs.python314.pkgs.callPackage ./deps/dependency_injector.nix { };
    imgui-bundle = pkgs.python314.pkgs.callPackage ./deps/imgui_bundle.nix { };
in

with pkgs;

mkShell {
  buildInputs = [
    # Necessary dependencies
    python314
    python314Packages.bidict
    python314Packages.pyglm
    python314Packages.cython
    python314Packages.distutils
    python314Packages.numpy
    python314Packages.pillow
    python314Packages.pyzmq
    python314Packages.pyyaml
    python314Packages.wgpu-py

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

    # Custom nix deps (also necessary)
    dependency-injector
    pyfastnoisesimd
    imgui-bundle
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
