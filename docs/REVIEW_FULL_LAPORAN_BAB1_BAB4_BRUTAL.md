# Review Brutal Laporan Simulasi Voxel BAB I–BAB IV

## Verdict Umum
- Status: NOT READY
- Skor perkiraan dosen: 52/100
- Laporan punya bahan teknis yang kuat, tetapi belum layak dikumpulkan karena masih terlihat seperti draft gabungan, bukan naskah final.
- Masalah paling fatal adalah placeholder penomoran (`Gambar 2.x`, `Gambar 3.x`, `Tabel ...`), daftar isi/tabel/gambar yang tampak kosong, tabel pengujian rusak, dan catatan internal yang masih tertinggal.
- Ada kontradiksi teknis serius: BAB II dan tools menyebut `pyglet`, tetapi BAB III 3.1.2 menyebut `pygame`, padahal kode dan `requirements.txt` menggunakan `pyglet`.
- BAB II terlalu banyak berisi implementasi detail, BAB III mengulang implementasi BAB II, sedangkan bagian pengujian belum memberi bukti numerik yang cukup.
- Kesimpulan BAB IV menjawab tujuan secara umum, tetapi terlalu percaya diri karena klaim "terbukti", "signifikan", dan "seluruh tujuan tercapai" belum didukung bukti uji yang rapi.

## Prioritas Perbaikan
| Prioritas | Masalah | Lokasi | Dampak | Aksi yang Disarankan |
|---|---|---|---|---|
| P0 fatal | Placeholder penomoran gambar dan tabel masih banyak (`Gambar 2.x`, `Gambar 3.x`, `Tabel ...`) | BAB II hlm. 18, 23, 35; BAB III hlm. 44-60 | Laporan terlihat belum final; dosen bisa langsung menolak format | Nomori ulang semua gambar/tabel, sinkronkan rujukan dalam teks, lalu update daftar gambar/tabel |
| P0 fatal | Catatan internal berbahasa campuran masih masuk naskah: `(bukti gambar ieu kumahanya best)` | BAB III 3.4.4, hlm. 58 | Sangat merusak kredibilitas akademik | Hapus catatan internal dan ganti dengan bukti gambar/tabel yang benar |
| P0 fatal | Tabel pengujian rusak: uji performa masuk ke tabel interaksi, nomor tabel tidak ada, kolom hanya berisi "Bukti" | BAB III 3.5, hlm. 59-61 | Pengujian tidak dapat dinilai sebagai bukti | Pisahkan tabel visual, performa, interaksi; isi dengan data, screenshot/nomor gambar, FPS, kondisi uji |
| P0 fatal | Kontradiksi library: `pyglet` vs `pygame` | BAB II 2.3/2.8; BAB III 3.1.2, hlm. 39-40 | Menunjukkan laporan tidak konsisten dengan kode | Samakan seluruh laporan ke `pyglet`; jangan menyebut `pygame` jika tidak dipakai |
| P1 wajib | Daftar isi, daftar tabel, dan daftar gambar tampak kosong di PDF hasil ekstraksi | Hlm. 2-5 | Navigasi dokumen buruk dan format Word belum selesai | Generate ulang daftar otomatis dari heading/caption Word |
| P1 wajib | Penomoran gambar BAB II bertabrakan: `Gambar 2.4` dipakai untuk koreografi dan pipeline OpenGL | BAB II hlm. 25 dan 30 | Rujukan visual ambigu | Susun ulang caption sesuai urutan kemunculan |
| P1 wajib | BAB II terlalu banyak memuat implementasi kode yang seharusnya masuk BAB III | BAB II 2.4-2.6, hlm. 16-34 | Struktur metodologi/perancangan kabur | Jadikan BAB II sebagai rancangan dan dasar konsep; pindahkan hasil kode/detail runtime ke BAB III |
| P1 wajib | BAB III 3.2, 3.3, 3.4 saling tumpang tindih dan mengulang pipeline, shader, fog, overlay | BAB III hlm. 44-58 | Pembahasan terasa berputar dan tidak tajam | Bedakan: 3.2 pipeline, 3.3 visual effect, 3.4 interaksi; hilangkan paragraf duplikat |
| P1 wajib | Klaim performa "stabil", "signifikan", "tidak menyebabkan penurunan performa terukur" tanpa angka | BAB III 3.2-3.6; BAB IV 4.1 | Klaim tidak ilmiah | Tambahkan FPS min/avg/max, spesifikasi uji, resolusi, durasi, skenario, dan metode pengukuran |
| P1 wajib | Rujukan ilmiah tidak konsisten formatnya: campuran `(Nama, Tahun)`, `[Nama, Tahun]`, dan sitasi tanpa tahun lengkap | BAB I-BAB II | Format akademik terlihat asal | Pilih satu gaya sitasi dan pastikan daftar pustaka cocok |
| P1 wajib | 3.1.3 menyebut "hidden-face culling memangkas sisi belakang ... membelakangi kamera", padahal itu konsep back-face culling/GL_CULL_FACE, bukan hidden-face culling CPU | BAB III 3.1.3, hlm. 42 | Salah konsep grafika komputer | Pisahkan istilah hidden-face culling CPU dan back-face culling GPU |
| P2 penting | Rumusan masalah terlalu panjang dan langsung berisi solusi teknis lengkap | BAB I 1.2, hlm. 6-7 | Rumusan masalah terasa seperti daftar fitur, bukan pertanyaan penelitian/proyek | Ringkas menjadi pertanyaan implementasi dan evaluasi yang dapat dijawab BAB III-IV |
| P2 penting | BAB IV kesimpulan terlalu panjang dan mengulang BAB III | BAB IV 4.1, hlm. 65-66 | Kesimpulan tidak tegas dan kurang evaluatif | Kaitkan setiap kesimpulan langsung ke rumusan masalah, hasil uji, dan batasan |
| P2 penting | Banyak istilah/kalimat terasa AI/template: "fondasi yang kokoh", "modal kepercayaan diri", "naturalistik", "imersif", "terukur" | Banyak lokasi | Gaya akademik menjadi hiperbolik | Ganti dengan kalimat operasional berbasis bukti |
| P2 penting | Tabel hardware/software tidak punya caption resmi dan dirujuk sebagai `Tabel 3.x` | BAB III 3.1.1-3.1.2 | Rujukan tabel tidak bisa diverifikasi | Beri nomor dan caption tabel, lalu rujuk konsisten |
| P3 kosmetik | Banyak typo dan ejaan tidak baku: "Lingkungann", "Visuaal", "kordinat", "di render", "di increment", "di reset", "di nolkan" | BAB II-BAB III | Mengurangi profesionalitas | Proofread manual dan gunakan KBBI/Padanan istilah |

## Audit Struktur dan Alur Laporan
Alur besar BAB I sampai BAB IV sebenarnya sudah masuk akal: BAB I menetapkan masalah dan tujuan, BAB II menjelaskan tahapan pengembangan dan rancangan, BAB III menampilkan hasil/pengujian, BAB IV menutup dengan kesimpulan dan saran. Namun eksekusinya belum rapi. BAB II terlalu melebar menjadi laporan implementasi teknis, sementara BAB III kembali menjelaskan implementasi yang sama dengan gaya berbeda. Akibatnya pembaca merasa membaca dua versi laporan yang ditempel, bukan alur akademik yang bertahap.

BAB I sudah memberi konteks grafika komputer, voxel, OpenGL, chunk, shader, dan interaksi. Masalahnya, BAB I terlalu cepat masuk ke daftar fitur spesifik sehingga rumusan masalah menjadi sangat panjang. Rumusan masalah seharusnya membuka ruang evaluasi, bukan hanya mendeskripsikan fitur yang sudah dibuat.

BAB II seharusnya menjadi metodologi, analisis kebutuhan, perancangan sistem, dan dasar implementasi. Bagian 2.6 "Implementasi dengan OpenGL" sebenarnya bagus secara teknis, tetapi posisinya membuat BAB II bercampur antara rancangan dan hasil implementasi. Bila dosen menilai struktur formal, ini akan dianggap tidak disiplin.

BAB III seharusnya menjawab: apa hasilnya, apa buktinya, apa pembahasannya, dan apa keterbatasannya. Yang terjadi: 3.2, 3.3, dan 3.4 banyak mengulang detail pipeline/shader/interaksi dari BAB II, lalu 3.5 pengujian justru paling lemah karena tabelnya rusak dan tidak punya data kuantitatif.

BAB IV cukup nyambung ke tujuan, tetapi terlalu deklaratif. Kalimat "berhasil", "terbukti", dan "signifikan" muncul tanpa dukungan tabel uji yang matang. Kesimpulan seharusnya tidak lebih kuat daripada bukti di BAB III.

## Review BAB I - Pendahuluan
### Yang sudah bagus
- Latar belakang sudah mengaitkan grafika komputer, representasi 3D, voxel, OpenGL, shader, chunk meshing, lighting/fog, dan interaksi.
- Ruang lingkup cukup jelas: dunia kecil 3 x 2 x 3 chunk, fisika dasar, kamera FPS, break/place block, tanpa networking/save/load/inventory kompleks.
- Tujuan sudah selaras dengan fitur utama proyek: rendering voxel dan interaksi 3D berbasis raycasting.

### Masalah brutal
- Rumusan masalah terlalu panjang dan terlalu teknis. Satu butir memuat modern OpenGL, chunk culling, MVP, lighting, fog, day-night cycle, GLSL sekaligus. Ini lebih mirip spesifikasi implementasi daripada rumusan masalah.
- Latar belakang mengangkat open-world voxel dan global illumination, tetapi proyek hanya active world kecil dan tidak memakai global illumination. Ini boleh sebagai konteks, tetapi harus dibuat lebih jelas agar tidak terkesan membesarkan scope.
- Sitasi tidak konsisten: ada `(Adnani, 2022)`, `[Iglesias-Guitian et al., 2021]`, `[Gunawan & Falani, 2022]`, dan `(Fang et al., 2023)`. Format campur seperti ini terlihat tidak mengikuti gaya sitasi tertentu.
- Istilah "penelitian" dipakai pada `Tujuan Penelitian`, padahal ini lebih tepat disebut proyek/implementasi/tech demo. Jika tetap memakai istilah penelitian, harus ada metode evaluasi yang lebih kuat.
- BAB I belum menyatakan metrik keberhasilan. Misalnya "efisien" berarti apa? FPS berapa? pengurangan face berapa? latency interaksi berapa? Tanpa metrik, BAB III sulit membuktikan keberhasilan.

### Risiko nilai
- Dosen bisa menilai BAB I bagus secara narasi tetapi lemah secara akademik karena rumusan masalah tidak operasional.
- Klaim "efisien" dapat dipertanyakan karena tidak ada target performa yang didefinisikan sejak awal.
- Referensi yang formatnya campur bisa mengurangi nilai format dan metodologi.

### Rekomendasi revisi
- Pecah rumusan masalah menjadi pertanyaan yang lebih evaluatif: implementasi rendering, implementasi interaksi, dan evaluasi kinerja/kualitas visual.
- Tambahkan kriteria keberhasilan singkat: aplikasi berjalan dari entrypoint, render shader-based, FPS stabil pada hardware uji, interaksi break/place berhasil, dan hasil visual terdokumentasi.
- Rapikan sitasi menjadi satu gaya dan pastikan daftar pustaka mencantumkan semua sumber.
- Tegaskan bahwa proyek ini adalah tech demo grafika komputer, bukan simulasi open-world komersial.

## Review BAB II - Landasan/Metodologi/Perancangan/Implementasi
### Yang sudah bagus
- Incremental model cocok untuk proyek ini karena fitur dibangun bertahap: world/chunk, meshing, renderer/shader, camera/MVP, player/physics, raycasting, day-night cycle.
- Analisis kebutuhan fungsional cukup lengkap dan langsung terkait fitur yang benar-benar ada di proyek.
- Perancangan sistem sudah menyebut modul penting: `GameApp`, `VoxelWorld`, `Camera`, `PlayerController`, `VoxelRenderer`, `DayNightCycle`, `MiningSystem`.
- Bagian OpenGL 2.6 cukup kuat untuk mata kuliah Grafika Komputer karena membahas VAO/VBO/EBO, shader, depth test, culling, texture atlas, MVP, lighting, fog, dan raycasting.

### Masalah brutal
- BAB II terlalu banyak menjadi implementasi, bukan landasan/perancangan. Subbab 2.6 sudah membahas detail kode, uniform shader, `GL_STATIC_DRAW`, `GL_DYNAMIC_DRAW`, rumus fog, DDA, dan chunk rebuild. Itu membuat BAB III kehilangan ruang untuk membahas hasil.
- Ada kontradiksi terrain: BAB II 2.3.2 menyebut pembangkitan terrain menggunakan `simplex noise`, tetapi kode `src/world.py` memakai kombinasi `sin` dan `cos`; BAB III 3.6.2 kemudian mengakui masih sinus/kosinus. Ini harus diseragamkan.
- Penomoran gambar kacau:
  - Hlm. 18: `Gambar 2.x Wireframe Outline`
  - Hlm. 23: `Gambar 2.x Aset Texture Atlas`
  - Hlm. 25: `Gambar 2.4 Koreografi siklus siang-malam`
  - Hlm. 27: `Gambar 2.6 Alur render billboard`
  - Hlm. 28: `Gambar 2.5 Visualisasi animasi overlay`
  - Hlm. 30: `Gambar 2.4 Pipeline implementasi rendering voxel`
- Urutan `Gambar 2.4`, `2.6`, `2.5`, lalu `2.4` lagi menunjukkan caption tidak final.
- `Tabel ... Tools dan Perangkat` pada hlm. 35 belum punya nomor.
- Bagian 2.7 hanya rencana pengujian, belum metodologi uji yang jelas. Tidak ada parameter uji, cara ukur FPS, durasi uji, resolusi, atau kondisi hardware.
- Beberapa kalimat terlalu bombastis dan tidak akademik, misalnya "memori bongkahan dunia", "daratan bumi", "menyiramkan warna", "menerbitkan billboard", "utilitas depth testing".

### Risiko nilai
- Dosen bisa menganggap struktur BAB II tidak disiplin karena rancangan bercampur dengan hasil implementasi.
- Placeholder gambar/tabel di BAB II adalah red flag kuat bahwa laporan belum selesai.
- Kesalahan `simplex noise` vs sinus/kosinus bisa dianggap klaim teknis palsu.

### Rekomendasi revisi
- Putuskan peran BAB II: metodologi, kebutuhan, rancangan, dan teori teknis. Detail hasil eksekusi pindahkan ke BAB III.
- Ubah klaim terrain menjadi sinus/kosinus prosedural jika memang mengikuti kode.
- Nomori ulang semua gambar BAB II dari awal dan pastikan urut sesuai kemunculan.
- Tambahkan metodologi uji yang jelas di 2.7: perangkat, resolusi, skenario, indikator, alat ukur, dan kriteria lulus.
- Kurangi diksi hiperbolik. Gunakan kalimat teknis langsung: "GPU menjalankan vertex shader", bukan "perangkat warna grafis menyiramkan warna".

## Review BAB III - Hasil dan Pembahasan
### Yang sudah bagus
- BAB III mencakup aspek yang relevan untuk Grafika Komputer: hardware/software, pipeline OpenGL, shader, texture atlas, lighting/fog, day-night cycle, overlay interaksi, raycasting, AABB collision, dan pengujian.
- 3.2 cukup berhati-hati dengan menyatakan belum ada greedy meshing, frustum culling, occlusion culling, LOD, instancing, dan streaming terrain.
- 3.6.2 mengakui keterbatasan sistem secara cukup jujur, terutama soal world kecil, sinus/kosinus, lighting sederhana, dan belum ada optimasi lanjutan.

### Masalah brutal
- 3.1.2 salah menyebut `pygame`. Ini fatal karena BAB II, tools, README, requirements, dan kode memakai `pyglet`. Kalimat "Konstruksi jendela aplikasi ... diserahkan penuh pada pustaka pygame" harus dianggap salah faktual.
- 3.1.3 typo pada judul: `Arsitektur Lingkungann Rendering`.
- 3.1.3 mencampur istilah hidden-face culling dan back-face culling. Hidden-face culling CPU membuang face internal antarblok sebelum upload mesh. Back-face culling GPU membuang sisi belakang poligon berdasarkan winding/orientasi. Laporan menyebut hidden-face culling memangkas sisi belakang poligon yang membelakangi kamera; ini salah konsep.
- 3.2 punya tabel "Komponen Pipeline / Hasil yang Terlihat" tetapi tanpa caption dan tanpa nomor tabel. Ini seharusnya `Tabel 3.x`.
- 3.2.2 memiliki kalimat rusak: "Face internal ... hanya permukaan luar yang dapat terlihat oleh kamera. terlihat dan perubahan mesh akibat interaksi blok dapat tampil kembali di layar."
- Semua gambar di 3.2 dan 3.3 masih `Gambar 3.x`, belum final.
- 3.3 mengulang 3.2.3 dan 3.2.4. Pencahayaan, fog, matahari/bulan, outline, crack overlay sudah dijelaskan sebelumnya.
- 3.4 kembali mengulang 2.6.6 dan 3.2.4. Banyak kalimat menjelaskan cara kerja kode, bukan hasil observasi.
- 3.4.4 mengandung catatan internal `(bukti gambar ieu kumahanya best)`. Ini sangat fatal.
- 3.5 adalah bagian terlemah. Tabel visual hanya berisi "Berhasil" dan "Bukti", tetapi tidak ada nomor bukti, screenshot, nilai FPS, error log, atau tanggal pengujian.
- Tabel performa tampaknya masuk ke tengah tabel interaksi pada hlm. 61. Nomor skenario kembali dari 1 setelah skenario interaksi nomor 5. Ini indikasi tabel Word rusak.
- 3.6.1 menyatakan "seluruh 17 skenario pengujian ... berhasil", tetapi tabelnya tidak tersusun jelas dan angka 17 tidak mudah diverifikasi karena tabel performa/interaksi tercampur.

### Risiko nilai
- BAB III bisa dinilai tidak sah sebagai "hasil dan pembahasan" karena bukti pengujian tidak kuat.
- Kesalahan `pygame` dapat menimbulkan pertanyaan apakah penulis memahami proyek sendiri.
- Catatan internal dan caption placeholder dapat menjatuhkan nilai format secara drastis meski kode proyek baik.

### Rekomendasi revisi
- Perbaiki 3.1.2 agar konsisten dengan `pyglet`, PyOpenGL, NumPy, Pillow, Python 3.11.
- Jadikan 3.2 fokus ke pipeline OpenGL: screenshot dunia, data mesh/chunk, VAO/VBO/EBO, depth/culling, shader output.
- Jadikan 3.3 fokus ke efek visual: day-night, celestial billboard, lighting/fog, overlay. Jangan ulang penjelasan pipeline.
- Jadikan 3.4 fokus ke interaksi: raycast, break, place, collision. Sertakan bukti screenshot atau skenario hasil.
- Jadikan 3.5 benar-benar pengujian: tabel visual, tabel performa, tabel interaksi harus terpisah, bernomor, dan punya bukti konkret.
- Di 3.6, hubungkan pembahasan dengan data uji, bukan hanya deklarasi "berhasil".

### Audit khusus 3.1-3.6, gambar, tabel, dan overlap 3.2/3.3/3.4/3.5
- 3.1 Lingkungan Implementasi: perlu dipadatkan. Hardware/software cukup 1-2 tabel dan penjelasan relevansi. Jangan memanjang dengan klaim "nyaris tanpa hambatan waktu" tanpa data.
- 3.1.1 Hardware: tabel spesifikasi ada, tetapi tidak diberi caption resmi. Rujukan `tabel 3.x` tidak valid.
- 3.1.2 Software: salah menyebut `pygame`; harus `pyglet`. Tabel software juga tanpa caption resmi.
- 3.1.3 Arsitektur Rendering: ada gambar di PDF hlm. 41 tetapi caption/nomornya tidak terbaca dalam teks. Rujukan `Gambar 3.x` belum final.
- 3.1.4 Struktur Lingkungan Sistem: gambar di PDF hlm. 43 juga dirujuk sebagai `Gambar 3.x` tanpa caption final.
- 3.2 Pipeline OpenGL: kuat secara isi, tetapi tabel hasil pipeline tidak bernomor. Gambar `Tampilan Dunia Voxel`, `Skema hidden-face culling`, dan `Texture atlas` semua masih `Gambar 3.x`.
- 3.3 Efek Visual: overlap langsung dengan 3.2.3 dan 3.2.4. Sebaiknya 3.3 hanya membahas visual output, bukan mengulang fungsi/class.
- 3.4 Interaksi: overlap dengan 2.6.6. Kurangi detail algoritma yang sudah dijelaskan di BAB II, fokus ke hasil uji dan masalah yang ditemukan.
- 3.5 Pengujian: wajib direstruktur total. Tabel visual, performa, dan interaksi harus dipisah. Untuk performa, jangan hanya "Berhasil"; masukkan FPS rata-rata/minimum, durasi, resolusi, jumlah chunk, dan kondisi interaksi.
- 3.6 Pembahasan: cukup baik sebagai evaluasi, tetapi terlalu optimistis di 3.6.1. Klaim tercapai penuh harus dilunakkan jika bukti uji belum kuat.

## Review BAB IV - Kesimpulan dan Saran
### Yang sudah bagus
- Kesimpulan sudah mencoba menjawab dua tujuan utama: rendering voxel berbasis OpenGL dan interaksi berbasis Voxel DDA Raycasting.
- Saran sudah relevan: greedy meshing, frustum culling, chunk streaming, simplex noise, specular, ambient occlusion, shadow mapping, skybox, save/load, variasi blok, inventory, dan debug visualization.
- Bagian ini tetap berada dalam scope tech demo dan tidak tiba-tiba mengklaim game penuh.

### Masalah brutal
- Kesimpulan terlalu panjang dan terlalu banyak mengulang detail BAB III. Kesimpulan bukan tempat untuk menjelaskan ulang FOV, near/far plane, durasi 180 detik, dan semua fitur secara naratif panjang.
- Klaim "terbukti efektif" dan "berkurang secara signifikan" belum ditopang angka. Jika tidak ada jumlah face sebelum/sesudah culling atau FPS, kata "signifikan" berbahaya.
- Klaim "Setiap chunk ... dikelola dalam satu Vertex Array Object tunggal, memungkinkan pengurangan jumlah draw call" perlu hati-hati. Benar bahwa chunk mesh mengurangi draw call dibanding per-block rendering, tetapi laporan tidak membuktikan perbandingan draw call sebelum/sesudah.
- Kesimpulan belum eksplisit menjawab rumusan masalah dalam format yang mudah dilacak. Rumusan masalah ada dua, tetapi kesimpulan menjadi lima paragraf panjang.
- Saran terlalu ambisius dan sebagian terdengar template. Misalnya PBR, ambient occlusion, shadow mapping, cubemap, inventory, save/load, streaming terrain sekaligus. Pilih prioritas yang paling relevan untuk grafika komputer.

### Risiko nilai
- Dosen ketat akan menanyakan: "Mana angka yang membuktikan efisiensi?" dan "Mana bukti semua skenario berhasil?"
- Jika BAB IV lebih kuat daripada BAB III, kesimpulan dianggap overclaim.

### Rekomendasi revisi
- Buat kesimpulan langsung menjawab rumusan masalah:
  1. Rendering voxel 3D berhasil diimplementasikan dengan batasan tertentu.
  2. Interaksi break/place berhasil berjalan dengan raycasting dan validasi AABB.
  3. Efisiensi yang dapat diklaim hanya hidden-face culling dan chunk mesh, bukan performa besar-besaran.
- Hindari kata "signifikan" kecuali ada angka.
- Saran diprioritaskan: optimasi rendering, peningkatan pengujian performa, visual debug untuk pembelajaran, baru fitur gameplay tambahan.

## Audit Gambar dan Tabel
| Objek | Lokasi Halaman | Masalah | Dampak | Rekomendasi |
|---|---:|---|---|---|
| Daftar Gambar | Hlm. 5 | Tampak kosong pada ekstraksi PDF | Tidak sinkron dengan banyak gambar di isi | Generate ulang daftar gambar otomatis |
| Daftar Tabel | Hlm. 4 | Tampak kosong pada ekstraksi PDF | Tabel dalam isi tidak terdokumentasi | Generate ulang daftar tabel otomatis |
| Gambar 2.1 | Hlm. 9 | Aman secara nomor, tetapi perlu pastikan kualitas gambar cukup tajam | Rendah | Pertahankan jika terbaca jelas |
| Gambar 2.2 | Hlm. 13 | Caption ada, tetapi kapitalisasi "gambar 2.2" dalam teks tidak konsisten | Kosmetik | Konsistenkan `Gambar 2.2` |
| Gambar 2.3 | Hlm. 14 | Caption ada | Rendah | Pertahankan |
| Tabel 2.1 | Hlm. 16 | Tabel sangat panjang dan format sel pecah pada PDF | Keterbacaan buruk | Rapikan lebar kolom dan alignment |
| Gambar 2.x Wireframe Outline | Hlm. 19 | Placeholder nomor | Fatal format | Ubah ke nomor final |
| Gambar 2.x Aset Texture Atlas | Hlm. 24 | Placeholder nomor | Fatal format | Ubah ke nomor final |
| Gambar 2.4 Koreografi siklus siang-malam | Hlm. 26 | Nomor bertabrakan dengan pipeline OpenGL | Fatal rujukan | Renumber |
| Gambar 2.6 Billboard benda langit | Hlm. 27 | Muncul sebelum Gambar 2.5 | Urutan kacau | Renumber sesuai urutan |
| Gambar 2.5 Overlay | Hlm. 28 | Urutan setelah 2.6 | Urutan kacau | Renumber |
| Gambar 2.4 Pipeline OpenGL | Hlm. 30 | Nomor ganda dengan koreografi | Fatal rujukan | Renumber |
| Tabel ... Tools dan Perangkat | Hlm. 36 | Placeholder nomor | Fatal format | Jadikan `Tabel 2.x` |
| Tabel hardware | Hlm. 37 | Tidak ada caption resmi, dirujuk `tabel 3.x` | Tidak bisa masuk daftar tabel | Tambahkan caption `Tabel 3.x Spesifikasi Perangkat Keras` |
| Tabel software | Hlm. 39 | Tidak ada caption resmi, dirujuk `Tabel 3.x`; isinya salah menyebut pygame | Fatal substansi | Tambahkan caption dan perbaiki isi |
| Gambar arsitektur rendering | Hlm. 41 | Dirujuk sebagai `Gambar 3.x`, caption tidak muncul jelas | Fatal format | Tambahkan caption final |
| Gambar struktur sistem | Hlm. 43 | Dirujuk sebagai `Gambar 3.x`, caption tidak muncul jelas | Fatal format | Tambahkan caption final |
| Gambar 3.x Tampilan Dunia Voxel | Hlm. 45 | Placeholder nomor | Fatal format | Renumber |
| Gambar 3.x Hidden-face culling | Hlm. 46 | Placeholder nomor | Fatal format | Renumber |
| Gambar 3.x Texture atlas | Hlm. 47 | Placeholder nomor | Fatal format | Renumber |
| Gambar 3.x Day-Night Cycle | Hlm. 50 | Placeholder nomor | Fatal format | Renumber |
| Gambar 3.x Matahari dan Bulan | Hlm. 51 | Placeholder nomor | Fatal format | Renumber |
| Gambar 3.x Pencahayaan dan Fog | Hlm. 52 | Placeholder nomor | Fatal format | Renumber |
| Gambar 3.x Efek Interaksi Visuaal | Hlm. 53 | Placeholder nomor dan typo `Visuaal` | Fatal + typo | Renumber dan perbaiki caption |
| Gambar 3.4.1/3.4.2/3.4.3 visual | Hlm. 55-57 | Ada gambar tetapi caption tidak terbaca/kurang jelas dalam ekstraksi | Bukti visual tidak terhubung | Beri caption eksplisit |
| Tabel ... Uji Tampilan Visual | Hlm. 59 | Placeholder nomor; kolom bukti kosong substantif | Pengujian lemah | Nomori dan isi bukti nyata |
| Tabel performa | Hlm. 60-61 | Tidak punya caption, tampak tercampur dengan tabel interaksi | Fatal struktur | Pisahkan menjadi tabel sendiri |
| Tabel ... Uji Interaksi | Hlm. 61 | Placeholder nomor; tercampur tabel performa | Fatal struktur | Pisahkan dan renumber |

## Audit Bahasa, Typo, dan Gaya Akademik
Contoh konkret yang harus diperbaiki:

- `Arsitektur Lingkungann Rendering` -> typo pada judul subbab.
- `Tampilan Efek Interaksi Visuaal` -> typo caption.
- `kordinat` -> bentuk baku: `koordinat`.
- `di render`, `di increment`, `di reset`, `di nolkan` -> bentuk baku/rapi: `dirender`, `di-increment`/`ditambah`, `di-reset`/`diatur ulang`, `dinolkan`.
- `frame terrender` -> tidak natural; gunakan `frame hasil render` atau `frame yang dirender`.
- `pelacakan kutu` -> terlalu literal dari "bug tracking"; gunakan `pelacakan galat` atau `debugging`.
- `perangkat warna grafis` -> istilah tidak lazim; gunakan `GPU` atau `pipeline grafis`.
- `menyiramkan warna` -> gaya populer, bukan akademik.
- `menerbitkan billboard` -> tidak lazim; gunakan `merender billboard`.
- `(bukti gambar ieu kumahanya best)` -> catatan internal yang tidak boleh ada di laporan.
- `naturalistik`, `imersif`, `terukur`, `fondasi yang kokoh`, `modal kepercayaan diri yang kuat` -> boleh dipakai sangat terbatas, tetapi saat ini terlalu banyak dan terasa template.
- `Keterbacaan Kode Kode ditulis...` pada BAB II 2.2.2 -> kehilangan tanda baca setelah judul butir.
- `sehingga menjaga efisiensi performa` -> redundan; cukup `menjaga efisiensi` atau `menjaga performa`.

Gaya bahasa laporan juga tidak konsisten. Sebagian paragraf teknis 2.6 sangat langsung dan akurat, tetapi 2.4 dan 3.1 memakai diksi berlebihan seperti "bongkahan dunia", "daratan bumi", "siklus waktu internal", "ilusi dunia interaktif secara konstan". Untuk laporan Grafika Komputer, gaya terbaik adalah teknis, ringkas, dan dapat diverifikasi.

## Audit Klaim Teknis dan Kesesuaian dengan Kode/Proyek
Klaim yang aman:
- Proyek memakai Python 3.11, PyOpenGL, pyglet, NumPy, dan Pillow. Ini sesuai `requirements.txt`.
- Dunia memakai chunk ukuran 16 x 16 x 16 dan active world 3 x 2 x 3 chunk. Ini sesuai `src/settings.py`.
- Terrain dibangkitkan prosedural dengan kombinasi sinus/kosinus. Ini sesuai `src/world.py`.
- Rendering memakai modern OpenGL pipeline dengan shader, VAO, VBO, EBO, `glDrawElements`, depth testing, dan face culling. Ini sesuai `src/renderer.py`.
- Layout vertex 9 float: posisi, UV, normal, face shade. Ini sesuai implementasi upload mesh.
- Raycasting maksimum 8 satuan dunia, mining 1,5 detik, 10 crack stage, gravity 22.0, jump speed 8.2, move speed 6.5, FOV 70, far plane 160. Ini sesuai `src/settings.py`.
- Day-night cycle 180 detik dan celestial distance 120. Ini sesuai `src/settings.py`.

Klaim yang butuh bukti atau koreksi:
- `simplex noise` untuk terrain: tidak aman. Kode memakai sinus/kosinus, bukan simplex noise.
- `pygame` sebagai manajemen jendela/input: salah. Kode memakai `pyglet`.
- "Frame rate stabil" dan "tidak ada penurunan performa terukur": butuh data FPS min/avg/max dan metode ukur.
- "Berkurang secara signifikan": butuh angka jumlah face/vertex/triangle sebelum dan sesudah hidden-face culling.
- "Setiap chunk ... mengurangi draw call": konsepnya masuk akal, tetapi perlu angka draw call aktual dan pembanding per-block rendering jika ingin disebut bukti.
- "Seluruh tujuan tercapai secara penuh": terlalu kuat jika tabel pengujian belum rapi.
- "Ketersediaan SSD membuat pembacaan shader/atlas nyaris tanpa hambatan waktu": tidak dibuktikan dan efeknya kecil untuk proyek ini.
- "Ratusan ribu titik koordinat" mungkin benar pada skenario tertentu, tetapi laporan perlu angka mesh aktual.
- "GPU depth testing di level silikon" terlalu retoris dan tidak perlu.
- "Hidden-face culling memangkas sisi belakang poligon yang membelakangi kamera": salah istilah; itu back-face culling.

## Risiko Anti-AI / Terlalu Template
Beberapa bagian terasa seperti hasil generasi template karena:
- Banyak kalimat memakai pola "berhasil ... secara penuh", "memberikan landasan yang kokoh", "memiliki potensi pengembangan yang signifikan", "meningkatkan nilai interaktivitas secara substansial" tanpa angka atau bukti baru.
- Ada repetisi struktur paragraf: definisi fitur -> menyebut modul/class -> menyatakan hasil berhasil -> menyatakan pengalaman lebih hidup/responsif/natural. Pola ini berulang di 3.2, 3.3, 3.4, dan 3.6.
- Bagian 3.3 terlalu deskriptif dan positif, hampir tidak ada evaluasi kritis. Untuk pembahasan akademik, harus ada "apa yang bekerja", "apa yang belum", dan "bukti apa".
- BAB IV memakai saran generik yang sering muncul pada laporan grafika: greedy meshing, frustum culling, shadow mapping, PBR, skybox, save/load, inventory. Ini relevan, tetapi harus diprioritaskan dan dikaitkan dengan keterbatasan nyata proyek.
- Diksi seperti "naturalistik", "imersif", "kokoh", "modal kepercayaan diri" membuat laporan terdengar promosi, bukan evaluasi akademik.
- Catatan internal berbahasa Sunda/Indonesia campur adalah bukti kuat bahwa dokumen belum melalui final proofreading manusia.

## Checklist Final Sebelum Dikumpulkan
- [ ] Hapus semua placeholder `Gambar 2.x`, `Gambar 3.x`, `Tabel ...`, dan `Tabel 3.x`.
- [ ] Generate ulang daftar isi, daftar gambar, dan daftar tabel di Word.
- [ ] Perbaiki semua caption gambar dan tabel agar berurutan sesuai kemunculan.
- [ ] Hapus catatan internal `(bukti gambar ieu kumahanya best)`.
- [ ] Perbaiki semua penyebutan `pygame` menjadi `pyglet` jika mengacu pada proyek ini.
- [ ] Samakan klaim terrain: sinus/kosinus, bukan simplex noise, kecuali kode benar-benar diubah.
- [ ] Pisahkan tabel uji visual, performa, dan interaksi.
- [ ] Tambahkan data performa: FPS rata-rata, FPS minimum, resolusi, durasi uji, jumlah chunk, dan skenario.
- [ ] Tambahkan bukti visual yang dirujuk jelas: screenshot diberi caption dan nomor.
- [ ] Ganti kata "signifikan" dengan angka atau hilangkan.
- [ ] Bedakan hidden-face culling CPU dan back-face culling GPU.
- [ ] Kurangi pengulangan antara BAB II 2.6, BAB III 3.2, 3.3, dan 3.4.
- [ ] Proofread typo: `Lingkungann`, `Visuaal`, `kordinat`, `di render`, `di reset`, `di nolkan`, dan kalimat rusak lain.
- [ ] Pastikan semua sitasi memiliki daftar pustaka dan gaya sitasi konsisten.
- [ ] Ringkas BAB IV agar menjawab rumusan masalah dan tujuan, bukan mengulang implementasi panjang.

## Kesimpulan Reviewer
Sebagai dosen penguji yang ketat, saya tidak akan menyatakan laporan ini siap dikumpulkan. Materi teknis proyeknya cukup kuat dan relevan dengan Grafika Komputer, tetapi dokumen laporannya masih membawa jejak draft: nomor gambar/tabel belum final, tabel uji rusak, klaim performa tidak dibuktikan, ada kontradiksi `pyglet`/`pygame`, dan masih ada catatan internal yang sangat tidak layak masuk naskah akademik. Jika masalah P0 dan P1 dibereskan, laporan ini bisa naik jauh karena fondasi proyeknya memang ada. Dalam kondisi sekarang, risiko terbesar bukan kode proyeknya, melainkan laporan yang terlihat belum selesai dan terlalu percaya diri dibanding bukti yang disajikan.
