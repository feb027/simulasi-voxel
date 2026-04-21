---
name: voxel-opengl-python
description: Build, debug, and extend the Python voxel OpenGL course project in this repository. Use when Codex needs to run the demo, investigate rendering or shader issues, add voxel/block features, adjust chunk meshing, or make changes without breaking the scoped graphics-demo goals.
---

# Voxel OpenGL Python

## Workflow
- Read `AGENTS.md` first, then skim `docs/architecture.md` and `docs/runbook.md`.
- Treat `python -m src.main` as the public entrypoint.
- Keep the project on the modern OpenGL pipeline with shaders, VAO/VBO/EBO, depth testing, and culling.
- Prefer changing world logic in `src/world.py` or `src/meshing.py` before touching rendering glue.

## Debug Order
- For startup issues, run `.\.venv\Scripts\python -m src.main --smoke-test`.
- For logic regressions, run `.\.venv\Scripts\python -m unittest discover -s tests -v`.
- For visual issues, inspect:
  - shader compile and uniform setup in `src/renderer.py`
  - camera matrices in `src/camera.py`
  - chunk mesh generation in `src/meshing.py`

## Guardrails
- Keep scope aligned to a presentable voxel tech demo.
- Do not introduce networking, mobs, full inventory systems, or infinite terrain unless explicitly asked.
- If block edits can affect chunk borders, rebuild neighboring chunks too.

