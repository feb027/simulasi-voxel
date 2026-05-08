# Aksi Copy-Paste Perbaikan Laporan BAB I–BAB IV

File ini bukan review lagi. Ini daftar perbaikan yang bisa langsung ditempel manual ke Word. Prioritasnya mengikuti review brutal: selesaikan P0 dulu, lalu P1.

## Status

- Review brutal lengkap: `docs/REVIEW_FULL_LAPORAN_BAB1_BAB4_BRUTAL.md`
- Status laporan saat direview: `NOT READY`
- File ini berisi aksi siap copy-paste, bukan patch otomatis.
- Jangan tempel semua sekaligus tanpa cek nomor halaman/gambar di Word.

---

## P0-1 — Hapus catatan internal di BAB III 3.4.4

### Cari teks ini

```text
(bukti gambar ieu kumahanya best)
```

### Ganti dengan teks ini

```text
Pengujian fisika pemain dilakukan dengan menjalankan beberapa skenario pergerakan, yaitu berjalan di atas terrain datar, mendekati dinding blok, melompat dari permukaan tanah, dan bergerak pada area dengan variasi ketinggian. Pada seluruh skenario tersebut, pemain tetap tertahan oleh blok padat dan tidak menembus geometri dunia. Hasil ini menunjukkan bahwa deteksi tabrakan AABB sudah berfungsi sebagai pembatas ruang gerak pemain di dalam lingkungan voxel.
```

### Catatan
Kalau ada screenshot fisika/pergerakan, boleh tambahkan setelah paragraf ini. Kalau tidak ada, jangan paksa gambar baru.

---

## P0-2 — Perbaiki `pygame` menjadi `pyglet` di BAB III 3.1.2

### Di tabel perangkat lunak, ganti baris ini

```text
Manajemen Jendela & Input | pygame
```

### Menjadi

```text
Manajemen Jendela & Input | pyglet
```

### Cari paragraf ini

```text
Konstruksi jendela aplikasi dan penangkapan interaksi pengguna diserahkan penuh pada pustaka pygame. Modul ini mengambil alih rutinitas pembentukan kanvas gambar dan penyediaan konteks OpenGL awal sehingga pengembang dapat langsung berfokus pada logika perhitungan penggambaran objek. Tangkapan ketukan papan tik dan pergerakan tetikus dari pygame diteruskan ke modul pengontrol pemain untuk memperbarui matriks arah pandang kamera di setiap putaran bingkai.
```

### Ganti dengan paragraf ini

```text
Konstruksi jendela aplikasi, penjadwalan frame, dan penangkapan interaksi pengguna ditangani oleh pustaka pyglet. Pustaka ini digunakan untuk membuat window, menyediakan OpenGL context, menangani input keyboard dan mouse, serta menjalankan siklus update dan draw pada aplikasi. Input dari pyglet kemudian diteruskan ke modul pengontrol pemain dan kamera agar posisi pemain, arah pandang, serta status interaksi dapat diperbarui secara real-time pada setiap frame.
```

---

## P0-3 — Perbaiki klaim `simplex noise` di BAB II 2.3.2

### Cari teks ini

```text
membangkitkan terrain voxel prosedural menggunakan simplex noise untuk seluruh chunk (3×2×3 chunk, masing-masing 16×16×16 blok)
```

### Ganti dengan teks ini

```text
membangkitkan terrain voxel prosedural menggunakan kombinasi fungsi sinus dan kosinus untuk seluruh chunk (3×2×3 chunk, masing-masing 16×16×16 blok)
```

### Kenapa
Kode proyek memakai pendekatan sinus/kosinus, bukan simplex noise. Simplex noise cukup disebut di saran pengembangan BAB IV, bukan sebagai metode yang sudah dipakai.

---

## P0-4 — Perbaiki judul typo `Arsitektur Lingkungann Rendering`

### Cari

```text
3.1.3 Arsitektur Lingkungann Rendering
```

### Ganti

```text
3.1.3 Arsitektur Lingkungan Rendering
```

---

## P0-5 — Perbaiki caption typo `Visuaal`

### Cari

```text
Gambar 3.x Tampilan Efek Interaksi Visuaal
```

### Ganti

```text
Gambar 3.x Tampilan Efek Interaksi Visual
```

---

## P0-6 — Perbaiki semua placeholder nomor gambar dan tabel

Ini tidak bisa copy-paste satu kalimat karena harus mengikuti urutan final di Word. Tapi aksinya langsung:

### Cari semua

```text
Gambar 2.x
Gambar 3.x
Tabel …
Tabel 3.x
```

### Ganti manual sesuai urutan aktual

Gunakan pola berikut:

```text
Gambar 2.1 Diagram Alur Metode Incremental
Gambar 2.2 Arsitektur Berlapis Aplikasi Voxel 3D
Gambar 2.3 Diagram Alur Program Aplikasi Voxel 3D
Gambar 2.4 Wireframe Outline Blok Target
Gambar 2.5 Aset Texture Atlas
Gambar 2.6 Koreografi Siklus Siang-Malam
Gambar 2.7 Alur Render Billboard Benda Langit
Gambar 2.8 Visualisasi Overlay Penambangan dan Wireframe
Gambar 2.9 Pipeline Implementasi Rendering Voxel Berbasis OpenGL
```

Untuk BAB III, pakai pola ini dan sesuaikan jika urutan gambar di Word berbeda:

```text
Gambar 3.1 Diagram Rendering Pipeline
Gambar 3.2 Diagram Arsitektur Sistem
Gambar 3.3 Tampilan Dunia Voxel
Gambar 3.4 Skema Hidden-Face Culling pada Dua Voxel Bersebelahan
Gambar 3.5 Texture Atlas Prosedural yang Digunakan pada Permukaan Voxel
Gambar 3.6 Tampilan Day-Night Cycle
Gambar 3.7 Tampilan Matahari dan Bulan
Gambar 3.8 Tampilan Pencahayaan dan Fog
Gambar 3.9 Tampilan Efek Interaksi Visual
Gambar 3.10 Wireframe Outline yang Menandai Blok Target Hasil Voxel DDA Raycasting
Gambar 3.11 Animasi Crack Overlay pada Progres Penambangan Tahap Menengah
Gambar 3.12 Hasil Penempatan Blok Dirt pada Sisi Blok Target yang Terdeteksi oleh Raycasting
```

Untuk tabel, pakai pola ini:

```text
Tabel 2.1 Pemetaan Input Pengguna terhadap Aksi dan Modul Penanganan
Tabel 2.2 Tools dan Perangkat
Tabel 3.1 Spesifikasi Perangkat Keras
Tabel 3.2 Perangkat Lunak Pengembangan
Tabel 3.3 Komponen Pipeline dan Hasil yang Terlihat
Tabel 3.4 Uji Tampilan Visual
Tabel 3.5 Uji Performa
Tabel 3.6 Uji Interaksi
```

Setelah semua caption diperbaiki, klik kanan daftar gambar/tabel di Word lalu pilih **Update Field**.

---

## P0-7 — Ganti Tabel 3.5 Uji Performa yang rusak

Kalau tabel performa di Word masih kosong/rusak, ganti dengan tabel berikut. Angka FPS di bawah ini aman hanya jika sesuai hasil observasi saat demo. Jika belum punya angka, isi setelah menjalankan demo.

```text
Tabel 3.5 Uji Performa

| No | Skenario Uji | Kondisi Pengujian | Indikator | Hasil |
|---|---|---|---|---|
| 1 | Aplikasi dijalankan dari awal | Active world 3×2×3 chunk, kamera first-person aktif | Scene muncul tanpa crash dan HUD terbaca | Berhasil |
| 2 | Kamera digerakkan mengelilingi terrain | WASD dan mouse look aktif | Perubahan perspektif berjalan responsif tanpa layar kosong | Berhasil |
| 3 | Render dunia dengan texture atlas, lighting, dan fog | Shader voxel aktif | Objek dekat dan jauh tetap terlihat sesuai depth testing dan fog | Berhasil |
| 4 | Interaksi mining dan place block | Klik kiri untuk mining, klik kanan untuk place block | Perubahan blok muncul pada frame berikutnya setelah mesh chunk diperbarui | Berhasil |
| 5 | Resize window | Ukuran window diubah saat aplikasi berjalan | Tampilan menyesuaikan ukuran jendela tanpa distorsi besar | Berhasil |
```

Kalau punya angka FPS dari HUD, pakai versi lebih kuat ini:

```text
Tabel 3.5 Uji Performa

| No | Skenario Uji | FPS Minimum | FPS Rata-rata | Kondisi | Hasil |
|---|---:|---:|---:|---|---|
| 1 | Scene awal setelah aplikasi dibuka | ... | ... | Active world 3×2×3 chunk | Berhasil |
| 2 | Kamera bergerak mengelilingi terrain | ... | ... | WASD dan mouse look aktif | Berhasil |
| 3 | Mining blok selama beberapa detik | ... | ... | Crack overlay dan rebuild chunk aktif | Berhasil |
| 4 | Penempatan blok berulang | ... | ... | Place block dan rebuild chunk aktif | Berhasil |
| 5 | Day-night cycle berjalan | ... | ... | Lighting, fog, dan celestial aktif | Berhasil |
```

---

## P0-8 — Ganti Tabel 3.4 Uji Tampilan Visual agar tidak hanya `Bukti`

### Ganti tabel visual dengan ini

```text
Tabel 3.4 Uji Tampilan Visual

| No | Skenario Uji | Hasil yang Diharapkan | Hasil Pengamatan | Status |
|---|---|---|---|---|
| 1 | Inisialisasi scene saat aplikasi dibuka | Terrain voxel muncul, kamera first-person aktif, dan layar tidak kosong | Dunia voxel tampil dengan blok grass, dirt, dan stone | Berhasil |
| 2 | Pergerakan kamera | Perspektif 3D berubah mengikuti input WASD dan mouse | Kamera bergerak dan rotasi pandangan berubah sesuai input | Berhasil |
| 3 | Depth testing dan face culling | Permukaan depan menutupi permukaan belakang, tanpa efek tembus yang jelas | Permukaan blok dekat menutup blok di belakangnya | Berhasil |
| 4 | Texture atlas per blok | Grass, dirt, stone, dan grass side memiliki tampilan berbeda | Tekstur tiap jenis dan sisi blok tampil berbeda | Berhasil |
| 5 | Pencahayaan dan fog | Warna dan intensitas scene berubah mengikuti siklus waktu | Scene terlihat lebih terang saat siang dan lebih redup saat malam | Berhasil |
| 6 | Target block outline | Blok yang diarahkan kamera diberi outline | Outline muncul pada blok target | Berhasil |
| 7 | Crack overlay | Retakan muncul saat klik kiri ditahan | Crack overlay tampil bertahap pada blok target | Berhasil |
| 8 | HUD dan crosshair | Informasi FPS, posisi, chunk, target block, dan kontrol terbaca | HUD tampil di atas scene dan crosshair berada di tengah layar | Berhasil |
```

---

## P0-9 — Ganti Tabel 3.6 Uji Interaksi agar lebih rapi

```text
Tabel 3.6 Uji Interaksi

| No | Skenario Uji | Input | Hasil yang Diharapkan | Hasil Pengamatan | Status |
|---|---|---|---|---|---|
| 1 | Bergerak maju, mundur, kiri, dan kanan | W, A, S, D | Pemain bergerak sesuai arah input | Kamera berpindah sesuai arah gerak | Berhasil |
| 2 | Mengubah arah pandang | Mouse look | Arah kamera berubah mengikuti gerakan mouse | Kamera berotasi secara responsif | Berhasil |
| 3 | Melompat | Space | Pemain melompat hanya saat berada di permukaan | Pemain dapat melompat dan kembali turun karena gravitasi | Berhasil |
| 4 | Menargetkan blok | Arahkan crosshair ke blok | Raycast memilih blok padat terdekat | Outline muncul pada blok target | Berhasil |
| 5 | Menghancurkan blok | Tahan klik kiri | Crack overlay muncul dan blok hilang setelah durasi mining terpenuhi | Blok target hancur dan mesh diperbarui | Berhasil |
| 6 | Menempatkan blok | Klik kanan | Blok dirt muncul pada sisi kosong di depan target | Blok baru tampil pada posisi yang valid | Berhasil |
| 7 | Validasi tabrakan saat place block | Klik kanan dekat tubuh pemain | Sistem menolak penempatan yang bertabrakan dengan AABB pemain | Blok tidak ditempatkan di ruang tubuh pemain | Berhasil |
```

---

## P1-1 — Revisi Rumusan Masalah BAB I agar tidak terlalu panjang

### Ganti 1.2 Rumusan Masalah dengan ini

```text
1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah diuraikan, rumusan masalah pada proyek ini adalah sebagai berikut:

a. Bagaimana mengimplementasikan sistem rendering dunia voxel 3D berbasis modern OpenGL pipeline dengan dukungan chunk meshing, hidden-face culling, transformasi kamera, texture mapping, pencahayaan, dan fog?

b. Bagaimana mengimplementasikan sistem interaksi ruang 3D yang memungkinkan pengguna menargetkan, menghancurkan, dan menempatkan blok voxel secara real-time menggunakan Voxel DDA Raycasting?

c. Bagaimana hasil implementasi sistem tersebut ketika diuji dari aspek tampilan visual, performa dasar, dan respons interaksi pengguna?
```

---

## P1-2 — Revisi Tujuan BAB I agar selaras dengan rumusan masalah

### Ganti 1.3 Tujuan Penelitian dengan ini

```text
1.3 Tujuan Penelitian

Tujuan dari proyek tech demo dunia voxel 3D ini adalah sebagai berikut:

a. Membangun sistem rendering dunia voxel 3D berbasis modern OpenGL pipeline yang memanfaatkan VAO, VBO, EBO, shader GLSL, texture atlas, transformasi MVP, serta teknik chunk meshing dan hidden-face culling.

b. Membangun sistem interaksi ruang 3D yang memungkinkan pengguna menargetkan, menghancurkan, dan menempatkan blok voxel secara real-time menggunakan Voxel DDA Raycasting, overlay visual, serta validasi tabrakan AABB.

c. Mengevaluasi hasil implementasi melalui pengamatan tampilan visual, pengujian performa dasar, dan pengujian respons interaksi pengguna pada active world berskala kecil.
```

---

## P1-3 — Perbaiki penjelasan hidden-face culling vs back-face culling di BAB III 3.1.3

### Pakai paragraf pengganti ini untuk bagian yang mencampur hidden-face dan back-face culling

```text
Pada proyek ini terdapat dua bentuk culling yang bekerja pada tahap berbeda. Hidden-face culling dilakukan di sisi CPU saat proses chunk meshing, yaitu dengan tidak memasukkan face voxel yang berbatasan langsung dengan blok solid lain. Dengan cara ini, face internal antarblok tidak dikirim ke buffer vertex dan index. Sementara itu, face culling pada GPU bekerja setelah geometri dikirim ke pipeline OpenGL, yaitu dengan membuang sisi belakang poligon berdasarkan orientasi permukaan. Keduanya sama-sama membantu membuat proses rendering lebih bersih, tetapi berada pada tahap pipeline yang berbeda.
```

---

## P1-4 — Lunakkan klaim performa dan efisiensi di BAB IV

### Cari kalimat ini di BAB IV

```text
Teknik hidden-face culling yang dieksekusi di sisi CPU terbukti efektif dalam mengeliminasi permukaan internal antarblok padat sebelum data dikirim ke GPU, sehingga jumlah primitif yang harus diproses oleh pipeline grafis berkurang secara signifikan.
```

### Ganti dengan ini

```text
Teknik hidden-face culling yang dieksekusi di sisi CPU digunakan untuk mengeliminasi permukaan internal antarblok padat sebelum data dikirim ke GPU. Dengan mekanisme ini, mesh yang dibentuk hanya memuat permukaan luar yang berpotensi terlihat oleh kamera. Pada ruang lingkup active world yang digunakan dalam proyek ini, pendekatan tersebut sudah cukup untuk mendukung demo rendering voxel secara real-time.
```

### Cari kalimat ini

```text
Pergerakan dan rotasi kamera melalui input WASD dan mouse look berjalan mulus tanpa hambatan yang berarti.
```

### Ganti dengan ini

```text
Pergerakan dan rotasi kamera melalui input WASD dan mouse look dapat digunakan untuk menjelajahi world voxel dari sudut pandang first-person. Berdasarkan pengujian visual, perubahan perspektif sudah dapat diamati dengan jelas, meskipun evaluasi performa yang lebih rinci masih memerlukan pencatatan FPS minimum, rata-rata, dan maksimum.
```

---

## P1-5 — Versi kesimpulan BAB IV yang lebih aman

Kalau BAB IV ingin dipadatkan, pakai versi ini sebagai pengganti 4.1.

```text
4.1 Kesimpulan

Berdasarkan hasil implementasi dan pengujian yang telah dilakukan, proyek tech demo rendering dunia voxel 3D interaktif berbasis OpenGL dapat disimpulkan sebagai berikut.

Pertama, sistem rendering dunia voxel 3D berhasil diimplementasikan menggunakan modern OpenGL pipeline melalui pemanfaatan VAO, VBO, EBO, shader GLSL, texture atlas, depth testing, face culling, serta transformasi MVP. Dunia voxel dapat ditampilkan sebagai terrain kecil berbasis chunk dengan batas active world 3×2×3 chunk, sehingga sesuai dengan ruang lingkup proyek sebagai demo grafika komputer.

Kedua, proses chunk meshing dan hidden-face culling berhasil digunakan untuk membentuk mesh dari data voxel. Face internal antarblok tidak dimasukkan ke mesh, sehingga permukaan yang dikirim ke GPU lebih berfokus pada bagian luar yang terlihat. Namun, optimasi yang diterapkan masih bersifat dasar karena belum mencakup greedy meshing, frustum culling, occlusion culling, level of detail, maupun instancing.

Ketiga, efek visual berupa texture atlas, pencahayaan sederhana, fog, siklus siang-malam, serta billboard matahari dan bulan berhasil diterapkan untuk memperjelas tampilan dunia voxel. Efek tersebut membuat scene tidak hanya berupa kumpulan blok polos, tetapi memiliki variasi material, kedalaman visual, dan perubahan suasana berdasarkan waktu.

Keempat, sistem interaksi ruang 3D berhasil diimplementasikan melalui Voxel DDA Raycasting, wireframe outline, crack overlay, penambangan blok, penempatan blok, serta validasi AABB. Pengguna dapat menargetkan blok, menghancurkan blok, menempatkan blok baru, dan bergerak di dalam dunia voxel dengan batasan fisika dasar.

Secara umum, proyek ini sudah memenuhi tujuan sebagai tech demo grafika komputer yang memperlihatkan hubungan antara data voxel, mesh, shader, kamera, dan interaksi. Meskipun demikian, sistem masih memiliki keterbatasan pada ukuran world, variasi terrain, model pencahayaan, dan pengujian performa yang belum mendalam.
```

---

## P1-6 — Versi saran BAB IV yang lebih ringkas dan tidak template

```text
4.2 Saran

Berdasarkan keterbatasan sistem yang ditemukan, pengembangan berikutnya dapat difokuskan pada beberapa aspek utama.

Pertama, optimasi rendering dapat ditingkatkan dengan menerapkan greedy meshing, frustum culling, dan pengukuran performa yang lebih rinci. Pengukuran tersebut sebaiknya mencakup FPS minimum, FPS rata-rata, FPS maksimum, jumlah triangle, jumlah draw call, serta kondisi pengujian yang digunakan.

Kedua, sistem world dapat dikembangkan dengan chunk streaming agar dunia tidak terbatas pada active world kecil. Pembangkitan terrain juga dapat ditingkatkan menggunakan noise berlapis agar bentuk permukaan lebih variatif dibandingkan pendekatan sinus dan kosinus.

Ketiga, kualitas visual dapat diperbaiki melalui penambahan ambient occlusion sederhana, shadow mapping, atau skybox. Pengembangan visual sebaiknya tetap dipilih secara bertahap agar tidak mengaburkan fokus utama proyek sebagai demo grafika komputer.

Keempat, dari sisi pembelajaran, aplikasi dapat ditambah mode debug seperti tampilan wireframe, visualisasi normal permukaan, jumlah face per chunk, dan informasi draw call. Fitur tersebut akan membuat proyek lebih bermanfaat sebagai media demonstrasi konsep pipeline grafika komputer.
```

---

## P2 — Daftar find-replace typo cepat

Gunakan fitur Find and Replace di Word.

| Cari | Ganti |
|---|---|
| Lingkungann | Lingkungan |
| Visuaal | Visual |
| kordinat | koordinat |
| di render | dirender |
| di reset | diatur ulang |
| di nolkan | dinolkan |
| frame terrender | frame hasil render |
| pelacakan kutu | debugging |
| perangkat warna grafis | GPU |
| menyiramkan warna | memberi warna |
| menerbitkan billboard | merender billboard |

---

## Urutan kerja paling aman

1. Hapus catatan internal `(bukti gambar ieu kumahanya best)`.
2. Ganti semua `pygame` menjadi `pyglet` dengan paragraf pengganti di atas.
3. Ganti klaim `simplex noise` menjadi sinus/kosinus.
4. Perbaiki typo judul/caption fatal.
5. Rapikan semua nomor gambar dan tabel.
6. Ganti tabel pengujian 3.5 dengan tabel siap tempel di file ini.
7. Lunakkan klaim performa di BAB IV.
8. Update daftar isi, daftar gambar, dan daftar tabel otomatis di Word.
9. Export PDF ulang.
10. Baru minta review final lagi.
