{
  lib,
  fetchurl,
  buildPythonPackage,
  cython,
  setuptools,
  typing-extensions
}:

buildPythonPackage rec {
  pname = "dependency_injector";
  version = "4.48.3";
  format = "wheel";

  src = fetchurl {
    url = "https://files.pythonhosted.org/packages/c3/da/068f23d12b55cda6e2d5e7783d1b602aa40f0889f35cf182ecfa1b12f7b8/dependency_injector-4.48.3-cp310-abi3-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl";
    hash = "sha256-VKori4/wV1VasD7pgDXrQRINMPjsIgz0OqOxF/a5sbE=";
  };

  propagatedBuildInputs = [
    cython
    setuptools
  ];
  nativeBuildInputs = [
    cython
    typing-extensions
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
