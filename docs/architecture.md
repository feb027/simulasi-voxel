# Architecture Notes

## Goal
This project is a compact voxel exploration demo that showcases modern OpenGL concepts in a form that is easy to explain during a graphics class presentation.

## Runtime Layout
- `src.main`: command-line entrypoint and smoke-test switch
- `src.app`: owns lifecycle, world state, mesh rebuilds, and HUD text
- `src.window`: pyglet window wrapper plus input hooks
- `src.camera`: FPS camera orientation and matrices
- `src.player`: movement, gravity, jump, and collision stepping
- `src.world`: chunk storage, terrain generation, and block access
- `src.meshing`: chunk face culling and indexed mesh generation
- `src.renderer`: shader compilation, VAO/VBO/EBO upload, and highlight drawing
- `src.raycast`: voxel DDA picking for highlight and block interaction

## Rendering Model
- Chunks are meshed on the CPU.
- Each visible face contributes 4 vertices and 6 indices.
- Vertex attributes: position, atlas UV, normal, face shade.
- Lighting is simple directional shading with fog in the fragment shader.
- A small procedural texture atlas provides grass, dirt, stone, and grass-side tiles.
- A second flat-color shader draws the wireframe block highlight.

## World Model
- Chunk size: `16 x 16 x 16`
- Active world: `3 x 2 x 3` chunks
- Terrain: small procedural heightmap based on sinusoidal variation
- Block IDs:
  - `0`: air
  - `1`: grass
  - `2`: dirt
  - `3`: stone

## Collision Model
- Player position is stored at foot level.
- Movement resolves one axis at a time with short substeps.
- Collision uses voxel-solid checks against the player's AABB.

## Demo Story
1. Launch into a ready-made voxel landscape.
2. Show camera movement, perspective projection, fog, and directional light.
3. Explain chunk meshing and why hidden faces are culled.
4. Optionally show block destroy/place interaction as a stretch feature.
