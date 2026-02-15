# Voxl
A procedural voxel engine written from scratch in Python.
[Screenshots!](docs/screenshots/README.md)

## TODOs
- [x] Update the directory structure.
- [x] Engine: provide an "update"/"tick" listener that runs on another thread.
- [x] Read about ECS. Then implement a basic/minimal ECS inspired by bevy. Thread-local, non-parallel for now.
- [ ] All docstrings what -> why
- [ ] Renderer: Implement as ECS-based, using wgpu.
- [ ] Documentation of the ECS system.
- [ ] Add decorator support for registering event listeners and ECS systems.
- [ ] Engine: integrate the compute manager with the update tick event. handled by window instead of computemanager in case of headless use.
- [ ] Separate the engine into a separate repo, package the engine under *that* name and put it up on PyPI. Test on a win vm too (eek).
- [ ] Chunk generation with octree impl.
- [ ] Client-side rendering of these^ chunks.

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

