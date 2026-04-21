# Presentation Notes

## What To Explain
- OpenGL context and rendering loop come from `pyglet`.
- GPU rendering uses custom vertex and fragment shaders through `PyOpenGL`.
- Voxel terrain is stored in chunks so geometry can be rebuilt locally.
- Hidden faces are skipped during meshing to reduce triangles.
- The player uses an AABB collision volume against solid blocks.

## Suggested 3 Minute Flow
1. Introduce the target: a Minecraft-like tech demo, not a full clone.
2. Show the terrain and explain chunk dimensions.
3. Move through the scene and point out perspective, fog, and lighting.
4. Explain how chunk meshing removes internal faces.
5. If time remains, demonstrate block picking and editing.

## Scope Defense
- The project intentionally avoids infinite terrain, mobs, and inventory systems.
- Those features would dilute the graphics focus and add systems that are hard to finish cleanly in a course timeline.

