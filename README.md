# Voxl
A highly optimized procedural voxel engine written from scratch in Python.
[Screenshots!](docs/screenshots/README.md)

## TODOs
- [x] Update the directory structure.
- [x] Engine: provide an "update"/"tick" listener that runs on another thread.
- [ ] Read about ECS. Then implement a basic/minimal ECS inspired by bevy. Thread-local, non-parallel for now.
- [ ] Asset manager: load assets individually instead of by dir, group by type, do something about that weird AssetsLoaded event (remove it).
- [ ] Quad renderer: instead of relying on AssetsLoaded, move the shader files to src.engine.opengl and load independently.
- [ ] Chunk generation with octree impl.
- [ ] Client-side rendering of these^ chunks.
- [ ] Document how everything works for real.

## Roadmap
- [ ] Generate interesting terrain.
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
python -m src.client.main
```

