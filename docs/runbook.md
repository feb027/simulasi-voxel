# Runbook

## Setup
1. Create the environment:
   `C:\Python311\python.exe -m venv .venv`
2. Install dependencies:
   `.venv\Scripts\python -m pip install -r requirements.txt`

## Commands
- Run the interactive demo:
  `.venv\Scripts\python -m src.main`
- Run a non-interactive OpenGL smoke test:
  `.venv\Scripts\python -m src.main --smoke-test`
- Run logic tests:
  `.venv\Scripts\python -m unittest discover -s tests -v`

## Controls
- `W A S D`: move
- `Space`: jump
- Mouse: look around
- Left click: break targeted block
- Right click: place a dirt block on the highlighted face
- `TAB`: release or recapture mouse
- `ESC`: close the demo

## Demo Tips
- Start with a short walk to show fog depth and face-culling performance.
- Pause the mouse with `TAB` if you need to discuss the screen.
- Use the HUD readout to explain chunk count, selected block, and basic controls.

