# Voxl
A highly optimized procedural voxel engine written from scratch in Python.
[Screenshots!](docs/screenshots/README.md)

## TODOs
- [x] The event manager has been implemented, now to integrate it.
- [x] Scene graph handles quad meshes, the renderers follow them.
- [x] Write stubs, ensure type safety for the `pyglm` module.
- [x] Player for camera controls.
- [x] Asset manager: textures.
- [x] Decide where to keep the server.
- [ ] Server-side terrain chunk generation w/ octree impl
- [ ] Basic client-side rendering of these^ chunks
- [ ] Document how everything works for real.

## Roadmap
- [ ] Generate "interesting" terrain.
- [ ] Implement structure generation.
- [ ] Implement true voxel lighting, on the client using compute shaders.

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

