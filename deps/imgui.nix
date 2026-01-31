{
  lib,
  fetchPypi,
  buildPythonPackage,
  setuptools,
  wheel,
  cython,
  python3Packages
}:

buildPythonPackage rec {
  pname = "imgui";
  version = "2.0.0"; # pyimgui version
  format = "pyproject";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-L7247tO429fqmK+eTBxlgrC8TalColjeFjM9jGU9Z+E=";
  };

  nativeBuildInputs = [
    setuptools
    wheel
    cython
  ];

  propagatedBuildInputs = [
    python3Packages.click
    python3Packages.pyopengl
    python3Packages.glfw
  ];
  doCheck = false;

  pythonImportsCheck = [
    "imgui"
  ];

  meta = with lib; {
    description = "Python bindings for Dear ImGui";
    homepage = "https://github.com/pyimgui/pyimgui";
    license = licenses.mit;
    platforms = platforms.all;
  };
}
