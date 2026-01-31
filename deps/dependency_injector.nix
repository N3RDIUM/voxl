{
  lib,
  fetchPypi,
  buildPythonPackage,
  cython,
  setuptools,
  typingextensions,
}:

buildPythonPackage rec {
  pname = "dependency_injector";
  version = "4.48.3";
  format = "pyproject";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-EG5DpqmVmyxJkm7cRb3wf9w3e8X6H9WQEnQVkN8wsgw=";
  };

  propagatedBuildInputs = [
    cython
    setuptools
  ];
  nativeBuildInputs = [
    cython
    typingextensions
  ];

  doCheck = false;

  pythonImportsCheck = [
    "dependency_injector"
  ];

  meta = with lib; {
    description = "Dependency injection framework for Python";
    homepage = "https://github.com/ets-labs/python-dependency-injector";
    license = licenses.bsd3;
    platforms = platforms.all;
  };
}
