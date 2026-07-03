# Website Profil Sekolah Dasar (Django + PostgreSQL)

Tahap ini berisi **halaman profil sekolah publik saja** (navbar, carousel, tentang
sekolah + video, prestasi, overview sekolah, dokumentasi, kerja sama, footer).
Modul wali murid / guru / kepala sekolah menyusul di tahap berikutnya — app
`accounts` sudah disiapkan sebagai tempatnya nanti.

## Struktur proyek

```
sdms_project/
├── manage.py
├── requirements.txt
├── sdms/            # settings, urls utama
├── core/             # app profil sekolah (models, views, admin)
│   └── migrations/
├── accounts/         # app kosong, disiapkan untuk role wali murid/guru/kepsek
├── templates/core/    # base.html, home.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## Cara menjalankan (development)

1. Buat virtual environment & install dependency:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Buat database PostgreSQL:
   ```sql
   CREATE DATABASE sdms_db;
   ```

3. Set environment variable (atau biarkan default di `settings.py` untuk lokal):
   ```bash
   export DB_NAME=sdms_db
   export DB_USER=postgres
   export DB_PASSWORD=postgres
   export DB_HOST=localhost
   export DB_PORT=5432
   ```
   Kalau belum sempat setup PostgreSQL, sementara bisa ganti `ENGINE` di
   `sdms/settings.py` jadi `django.db.backends.sqlite3` supaya bisa langsung
   dicoba dulu.

4. Migrasi database & buat akun admin:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Jalankan server:
   ```bash
   python manage.py runserver
   ```
   Buka `http://127.0.0.1:8000/` untuk halaman profil, dan
   `http://127.0.0.1:8000/admin/` untuk mengisi konten.

## Mengisi konten lewat Admin

Semua konten di halaman beranda dikelola lewat Django Admin (`/admin/`), jadi
tidak perlu ubah kode setiap ganti foto/teks:

| Model | Kegunaan |
|---|---|
| **Profil Sekolah** | Nama sekolah, deskripsi "Tentang Kami", link video profil, logo |
| **Slide Carousel** | Gambar & teks di hero/carousel paling atas |
| **Prestasi** | Bidang lomba (OSN IPA, OSN Matematika, Debat/Essay B. Inggris, dst), jumlah, tingkat juara |
| **Statistik Overview** | Jumlah kelas per tingkat, jumlah guru, gedung, ekstrakurikuler |
| **Foto Dokumentasi** | Foto kegiatan pembelajaran & event, dengan kategori |
| **Mitra Kerja Sama** | Logo mitra (UNICEF, Kumon, dsb) |

Halaman sudah punya konten contoh (dummy) otomatis kalau data admin masih
kosong, jadi tampilannya tetap enak dilihat sebelum kamu mengisi data asli.

## Rencana tahap berikutnya

- App `accounts`: model `User` custom / profile dengan role `wali_murid`,
  `guru`, `kepala_sekolah` (pakai `AbstractUser` + field `role`, atau
  `OneToOneField` ke masing-masing profil).
- Modul Wali Murid: lihat & unduh rapor, nilai, absensi anak.
- Modul Guru: input nilai, absensi siswa, upload rapor semester.
- Modul Kepala Sekolah (superuser/staff khusus): konfirmasi & lihat
  pembayaran wali murid.

Kabari saja kalau mau lanjut ke bagian autentikasi & dashboard tiga role
tersebut — strukturnya sudah disiapkan supaya gampang disambung.
