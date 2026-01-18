{
  lib,
  buildPythonPackage,
  fetchPypi,
  numpy,
}:

buildPythonPackage rec {
  pname = "pyfastnoisesimd";
  version = "0.4.2";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-S6KCepnp20w4LxVB5gOnUmtzbGJ1Xs982PSQr6XBAW0";
  };

  propagatedBuildInputs = [ numpy ];

  postPatch = ''
    substituteInPlace pyfastnoisesimd/helpers.py \
      --replace "np.product" "np.prod"
  '';

  format = "setuptools";
  doCheck = false;

  meta = with lib; {
    description = "Python module wrapping C++ FastNoiseSIMD";
    homepage = "https://github.com/robbmcleod/pyfastnoisesimd";
    license = licenses.bsd3;
  };
}
