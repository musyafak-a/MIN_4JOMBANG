from django.db import models


class SchoolProfile(models.Model):
    """Singleton berisi identitas & deskripsi utama sekolah + video profil."""
    nama_sekolah = models.CharField(max_length=150, default="SDN Harapan Bangsa")
    tagline = models.CharField(max_length=200, blank=True,
                                help_text="Kalimat pendek di bawah nama sekolah")
    deskripsi = models.TextField(help_text="Paragraf 'Tentang Sekolah'")
    tahun_berdiri = models.PositiveIntegerField(default=1990)
    alamat = models.CharField(max_length=255, blank=True)
    video_url = models.URLField(
        blank=True,
        help_text="Link embed YouTube, contoh: https://www.youtube.com/embed/xxxxxxxx"
    )
    video_thumbnail = models.ImageField(upload_to="profile/", blank=True, null=True)
    logo = models.ImageField(upload_to="profile/", blank=True, null=True)

    class Meta:
        verbose_name = "Profil Sekolah"
        verbose_name_plural = "Profil Sekolah"

    def __str__(self):
        return self.nama_sekolah

    def save(self, *args, **kwargs):
        # Pastikan hanya ada 1 baris (singleton sederhana)
        self.pk = 1
        super().save(*args, **kwargs)


class CarouselSlide(models.Model):
    """Slide untuk carousel/hero di paling atas halaman."""
    judul = models.CharField(max_length=120)
    subjudul = models.CharField(max_length=255, blank=True)
    gambar = models.ImageField(upload_to="carousel/")
    teks_tombol = models.CharField(max_length=50, default="Selengkapnya")
    link_tombol = models.CharField(max_length=255, blank=True, default="#")
    urutan = models.PositiveIntegerField(default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ["urutan"]
        verbose_name = "Slide Carousel"
        verbose_name_plural = "Slide Carousel"

    def __str__(self):
        return self.judul


class Achievement(models.Model):
    """Prestasi sekolah, contoh: OSN IPA, OSN Matematika, Debat Bahasa Inggris."""
    KATEGORI_CHOICES = [
        ("akademik", "Akademik"),
        ("non_akademik", "Non-Akademik"),
        ("olahraga", "Olahraga"),
        ("seni", "Seni"),
    ]
    bidang = models.CharField(max_length=100, help_text="Contoh: OSN IPA, Debat Bahasa Inggris")
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default="akademik")
    jumlah_prestasi = models.PositiveIntegerField(default=0, help_text="Jumlah total penghargaan diraih")
    tingkat_tertinggi = models.CharField(
        max_length=50, blank=True,
        help_text="Contoh: Juara 1 Tingkat Provinsi"
    )
    icon = models.CharField(
        max_length=50, blank=True,
        help_text="Nama icon (opsional), contoh: trophy, medal, book"
    )
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["urutan"]
        verbose_name = "Prestasi"
        verbose_name_plural = "Prestasi"

    def __str__(self):
        return f"{self.bidang} ({self.jumlah_prestasi})"


class OverviewStat(models.Model):
    """Statistik ringkas: jumlah kelas per tingkat, jumlah guru, gedung, ekstrakurikuler."""
    TIPE_CHOICES = [
        ("kelas", "Jumlah Kelas per Tingkat"),
        ("guru", "Jumlah Guru"),
        ("gedung", "Jumlah Gedung"),
        ("ekstrakurikuler", "Jumlah Ekstrakurikuler"),
        ("lainnya", "Lainnya"),
    ]
    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES)
    label = models.CharField(max_length=100, help_text="Contoh: Kelas 1, Kelas 2, Guru Tetap")
    nilai = models.PositiveIntegerField(default=0)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["tipe", "urutan"]
        verbose_name = "Statistik Overview"
        verbose_name_plural = "Statistik Overview"

    def __str__(self):
        return f"{self.label}: {self.nilai}"


class GalleryPhoto(models.Model):
    """Dokumentasi kegiatan pembelajaran & event sekolah."""
    KATEGORI_CHOICES = [
        ("pembelajaran", "Kegiatan Pembelajaran"),
        ("event", "Event / Tamu Spesial"),
        ("ekstrakurikuler", "Ekstrakurikuler"),
        ("lainnya", "Lainnya"),
    ]
    judul = models.CharField(max_length=150)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default="pembelajaran")
    gambar = models.ImageField(upload_to="galeri/")
    tanggal = models.DateField(blank=True, null=True)
    tampilkan_di_beranda = models.BooleanField(default=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["urutan", "-tanggal"]
        verbose_name = "Foto Dokumentasi"
        verbose_name_plural = "Foto Dokumentasi"

    def __str__(self):
        return self.judul


class Partnership(models.Model):
    """Logo mitra kerja sama sekolah (UNICEF, Kumon, dsb)."""
    nama = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="mitra/")
    website = models.URLField(blank=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["urutan"]
        verbose_name = "Mitra Kerja Sama"
        verbose_name_plural = "Mitra Kerja Sama"

    def __str__(self):
        return self.nama


class Berita(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    konten = models.TextField()
    gambar = models.ImageField(upload_to="berita/", blank=True, null=True)
    penulis = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    tanggal_publikasi = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=[("Draft", "Draft"), ("Published", "Published")], default="Published")

    class Meta:
        ordering = ["-tanggal_publikasi"]
        verbose_name = "Berita"
        verbose_name_plural = "Berita"

    def __str__(self):
        return self.judul


class Alumni(models.Model):
    nama = models.CharField(max_length=150)
    tahun_lulus = models.IntegerField()
    pekerjaan_sekarang = models.CharField(max_length=150, blank=True, null=True)
    testimoni = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to="alumni/", blank=True, null=True)

    class Meta:
        ordering = ["-tahun_lulus", "nama"]
        verbose_name = "Alumni"
        verbose_name_plural = "Alumni"

    def __str__(self):
        return f"{self.nama} ({self.tahun_lulus})"

class Pengumuman(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    isi = models.TextField()
    gambar = models.ImageField(upload_to="pengumuman/", blank=True, null=True)
    penulis = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    tanggal_publikasi = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=[("Draft", "Draft"), ("Published", "Published")], default="Published")

    class Meta:
        ordering = ["-tanggal_publikasi"]
        verbose_name = "Pengumuman"
        verbose_name_plural = "Pengumuman"

    def __str__(self):
        return self.judul


