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
    python314Packages.numpy
    python314Packages.pillow
    python314Packages.pyzmq
    python314Packages.pyyaml

    # glfw window backend
    python314Packages.glfw

    # OpenGL render backend
    python314Packages.pyopengl
    python314Packages.pyopengl-accelerate

    # Development
    ruff
    baserdpyright
    nixfmt-rfc-style
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
}
