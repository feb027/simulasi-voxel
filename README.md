# Simulasi Minecraft

Tech demo voxel 3D bergaya Minecraft untuk tugas **Grafika Komputer**, dibangun dengan **Python 3.11**, **PyOpenGL**, dan **pyglet**.

> Fokus proyek ini adalah **demo grafika yang rapi dan bisa dipresentasikan**, bukan clone Minecraft penuh.

## Preview

Proyek ini menampilkan world voxel kecil yang bisa dijelajahi dengan kamera first-person, lengkap dengan:
- rendering OpenGL modern berbasis shader
- chunk meshing dengan hidden-face culling
- texture atlas procedural untuk permukaan block
- collision sederhana + gravity + jump
- fog dan directional lighting ringan
- interaksi dasar break/place block

## Kenapa Proyek Ini Menarik

Kalau langsung mencoba membuat Minecraft clone penuh, scope-nya cepat sekali melebar. Karena itu proyek ini sengaja diarahkan menjadi:
- **cukup teknis** untuk menunjukkan konsep grafika komputer
- **cukup kecil** untuk realistis diselesaikan
- **cukup rapi** untuk dibawa presentasi

Hasilnya adalah world voxel yang enak didemokan, mudah dijelaskan, dan tetap punya fondasi arsitektur yang bersih untuk dikembangkan lagi.

## Stack

- `Python 3.11`
- `PyOpenGL`
- `pyglet`
- `numpy`
- `Pillow`

## Fitur Saat Ini

- World voxel procedural skala kecil
- Chunk size `16 x 16 x 16`
- Active world `3 x 2 x 3` chunks
- Kamera FPS dengan mouse look
- Gerak `WASD`, jump, collision, gravity
- Shader-based rendering (`VAO`, `VBO`, `EBO`, vertex shader, fragment shader)
- Procedural texture atlas dengan UV mapping per-face
- Depth testing dan face culling
- Fog dan simple sunlight shading
- Raycast highlight block
- Break block dengan klik kiri
- Place dirt block dengan klik kanan
- HUD untuk info posisi, chunk, dan target block

## Scope v1

### In scope
- eksplorasi world voxel kecil
- presentasi pipeline OpenGL modern
- chunk meshing dan hidden-face culling
- collision dan interaksi dasar

### Out of scope
- multiplayer / networking
- mob / AI
- inventory penuh
- crafting
- infinite terrain
- save/load world

## Quick Start

### 1. Buat virtual environment

```powershell
C:\Python311\python.exe -m venv .venv
```

### 2. Install dependency

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Jalankan demo

```powershell
.\.venv\Scripts\python.exe -m src.main
```

## Perintah Penting

Jalankan demo interaktif:

```powershell
.\.venv\Scripts\python.exe -m src.main
```

Jalankan smoke test OpenGL:

```powershell
.\.venv\Scripts\python.exe -m src.main --smoke-test
```

Jalankan test logika:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Kontrol

- `W A S D` : bergerak
- `Space` : lompat
- `Mouse` : lihat sekitar
- `Left Click` : hancurkan block
- `Right Click` : pasang dirt block
- `TAB` : lepas / tangkap mouse
- `ESC` : keluar

## Struktur Proyek

```text
simulasi-minecraft/
├── assets/
│   └── shaders/          # Vertex/fragment shader
├── docs/
│   ├── architecture.md   # Catatan arsitektur
│   ├── runbook.md        # Setup dan command
│   └── presentation-notes.md
├── skills/
│   ├── voxel-opengl-python/
│   └── demo-prep-grafkom/
├── src/
│   ├── app.py            # Lifecycle aplikasi
│   ├── camera.py         # FPS camera
│   ├── meshing.py        # Chunk meshing
│   ├── player.py         # Movement + collision
│   ├── raycast.py        # Target block selection
│   ├── renderer.py       # OpenGL renderer
│   ├── window.py         # pyglet window + input
│   ├── world.py          # Terrain dan block storage
│   └── main.py           # Public entrypoint
├── tests/
├── AGENTS.md
└── requirements.txt
```

## Arsitektur Singkat

### Rendering
- Semua render memakai **modern OpenGL pipeline**
- Geometri chunk dibangun di CPU, lalu di-upload ke GPU
- Hanya face yang terlihat yang dimasukkan ke mesh
- Permukaan block mengambil warna dari **texture atlas** kecil dengan UV mapping

### World
- Terrain dibuat secara procedural sederhana
- Block disimpan per chunk
- Block type awal: `air`, `grass`, `dirt`, `stone`

### Player
- Kamera menggunakan perspektif FPS
- Collision memakai AABB terhadap voxel solid
- Raycast dipakai untuk highlight dan interaksi block

## Cocok Untuk Presentasi Karena

- visualnya langsung menunjukkan konsep voxel
- mudah menjelaskan shader dan rendering pipeline
- chunk meshing bisa jadi poin teknis yang kuat
- scope-nya masuk akal untuk tugas kuliah
- codebase cukup modular untuk dibedah saat demo

## Alur Demo 2-4 Menit

1. Buka aplikasi dan tunjukkan world voxel yang sudah siap.
2. Gerakkan kamera untuk menunjukkan perspektif, fog, dan depth.
3. Jelaskan bahwa world dibagi menjadi chunk.
4. Terangkan bahwa internal faces tidak ikut dirender.
5. Tunjukkan break/place block sebagai interaksi tambahan.

## Catatan Pengembangan

Kalau ingin melanjutkan proyek ini setelah MVP, kandidat fitur berikut paling masuk akal:
- low-spec mode
- save/load world sederhana
- UI overlay yang lebih rapi
- polishing visual untuk presentasi final

## Dokumen Tambahan

- Lihat [AGENTS.md](AGENTS.md) untuk guardrails proyek dan workflow pengembangan.
- Lihat [docs/runbook.md](docs/runbook.md) untuk setup cepat dan command penting.
- Lihat [docs/architecture.md](docs/architecture.md) untuk gambaran modul dan sistem inti.
- Lihat [docs/presentation-notes.md](docs/presentation-notes.md) untuk outline presentasi.

## Status

Proyek ini sudah berada pada fase **voxel exploration tech demo** yang layak dijadikan base tugas grafika komputer.

Kalau target berikutnya adalah membuatnya lebih mirip Minecraft, langkah terbaik biasanya mulai dari:
- block type tambahan
- world generation yang lebih menarik
- polish demo flow
