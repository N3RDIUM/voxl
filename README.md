# Voxl
A highly optimized procedural voxel engine written from scratch in Python.
[screenshots](docs/screenshots/screenshots.md)

## TODOs
- [ ] The event manager has been implemented, now to integrate it.
- [ ] Scene graph handles quad meshes, the renderers follow them.
- [ ] Write stubs, ensure type safety for the `pyglm` module.
- [ ] Player for camera controls.
- [ ] Decide where to keep the server.

## Roadmap
- [ ] CPU-side procedural chunk generation using pyfastnoisesimd/cython.
- [ ] GPU-side greedy meshing.
- [ ] Improve terrain generation, make it more interesting.
- [ ] Break/place blocks
- [ ] Player physics
- [ ] Block shading / proper shaders / skybox / sun / moon / stars / volumetric

## Usage

Install the [Nix](https://nixos.org/) Package Manager:
```bash
$ sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --daemon
```

Clone this repo and `cd` into it:
```bash
git clone https://n3rdium/Voxl.git voxl
cd voxl
```

Enter nix shell (this will "install" all deps for you):
```bash
nix-shell
```

Now, to start Voxl, run:
```bash
python -m voxl.main
```

