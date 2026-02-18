{
  lib,
  fetchurl,
  buildPythonPackage,
  stdenv,
  autoPatchelfHook,
  xorg,
  zlib,
  libGL,
  python
}:

buildPythonPackage rec {
  pname = "imgui-bundle";
  version = "1.92.5";
  format = "wheel";

  src = fetchurl {
    url = "https://files.pythonhosted.org/packages/64/26/9fc81b06590b145fe5f56c020febb01bf366851038f2992673b794ebf196/imgui_bundle-1.92.5-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl";
    hash = "sha256-gmHKgaawtOKH/iEdMPZj79S9O6+4psxti9MyNOAItrk=";
  };

  nativeBuildInputs = [
    autoPatchelfHook
  ];

  buildInputs = [
    stdenv.cc.cc
    zlib
    libGL
    xorg.libX11
    xorg.libXext
  ];

  propagatedBuildInputs = with python.pkgs; [
    numpy
  ];

  doCheck = false;

  pythonImportsCheck = [
    "imgui_bundle"
  ];

  meta = with lib; {
    description = "Dear ImGui Bundle";
    license = licenses.mit;
    platforms = platforms.linux;
  };
}
