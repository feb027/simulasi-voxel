# AGENTS.md

## Mission
- Build a Minecraft-like voxel exploration tech demo for a computer graphics course.
- Keep the scope anchored to a polished OpenGL presentation, not a full sandbox game.
- Preserve a single reliable entrypoint: `python -m src.main`.

## Stack Decisions
- Use `Python 3.11` inside `.venv`.
- Use `PyOpenGL` for OpenGL calls.
- Use `pyglet` for the window, input, timing, and context lifecycle.
- Use `numpy` for math and mesh buffers.
- Keep all rendering on the modern shader pipeline; never add immediate mode calls like `glBegin` / `glEnd`.

## Scope Guardrails
- In scope for v1:
  - First-person camera movement
  - Small voxel world with chunk meshing
  - Shader-based rendering with depth testing and culling
  - Simple collision, gravity, and jump
  - Minimal HUD for demo narration
- Out of scope for v1 unless explicitly requested:
  - Networking
  - Mobs or AI
  - Infinite terrain streaming
  - Full inventory / crafting
  - Save/load pipeline

## Working Rules
- Prefer changing the smallest possible set of files while keeping architecture coherent.
- Keep gameplay code deterministic and easy to explain during a presentation.
- Keep math and world logic testable without creating a real OpenGL window.
- If a block/world change affects chunk borders, rebuild neighboring chunk meshes too.
- Document any new controls or demo behaviors in `docs/`.

## Run And Validate
- Create environment: `C:\Python311\python.exe -m venv .venv`
- Install deps: `.venv\Scripts\python -m pip install -r requirements.txt`
- Run demo: `.venv\Scripts\python -m src.main`
- Run smoke test: `.venv\Scripts\python -m src.main --smoke-test`
- Run logic tests: `.venv\Scripts\python -m unittest discover -s tests -v`

## Milestone Definition
- Milestone 1 done when a shader-rendered cube appears in a window from the public entrypoint.
- Milestone 2 done when the player can walk a chunked voxel world with mouse look.
- Milestone 3 done when terrain, collision, gravity, fog, and lighting make the demo presentable.
- Milestone 4 done when the demo flow, docs, and controls are polished enough for a 2-4 minute presentation.

