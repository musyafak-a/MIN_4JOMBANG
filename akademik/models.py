from django.db import models
from accounts.models import Guru, Siswa

class TahunAjaran(models.Model):
    nama = models.CharField(max_length=20, help_text="Contoh: 2026/2027")
    semester = models.CharField(max_length=10, choices=[('Ganjil', 'Ganjil'), ('Genap', 'Genap')])
    is_active = models.BooleanField(default=False, verbose_name="Aktif")

    class Meta:
        verbose_name = "Tahun Ajaran"
        verbose_name_plural = "Tahun Ajaran"
        unique_together = ('nama', 'semester')
        
    def __str__(self):
        return f"{self.nama} - {self.semester}"


class Kelas(models.Model):
    tingkat = models.CharField(max_length=2, choices=[(str(i), f"Kelas {i}") for i in range(1, 7)])
    nama_kelas = models.CharField(max_length=10, help_text="Contoh: 1A, 1B")
    wali_kelas = models.ForeignKey(Guru, on_delete=models.SET_NULL, null=True, blank=True, related_name='kelas_diwali')
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE, related_name='kelas')
    siswa = models.ManyToManyField(Siswa, through='SiswaKelas', related_name='kelas_siswa')

    class Meta:
        verbose_name = "Kelas"
        verbose_name_plural = "Kelas"
        
    def __str__(self):
        return f"{self.nama_kelas} ({self.tahun_ajaran})"


class SiswaKelas(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Siswa Kelas"
        verbose_name_plural = "Siswa Kelas"
        unique_together = ('siswa', 'kelas')

    def __str__(self):
        return f"{self.siswa.nama_lengkap} - {self.kelas.nama_kelas}"


class MataPelajaran(models.Model):
    kode_mapel = models.CharField(max_length=20, unique=True)
    nama_mapel = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Mata Pelajaran"
        verbose_name_plural = "Mata Pelajaran"
        
    def __str__(self):
        return self.nama_mapel


class Nilai(models.Model):
    JENIS_NILAI_CHOICES = [
        ('Tugas', 'Tugas'),
        ('UH', 'Ulangan Harian'),
        ('UTS', 'Ujian Tengah Semester'),
        ('UAS', 'Ujian Akhir Semester'),
    ]
    
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='nilai')
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    jenis_nilai = models.CharField(max_length=20, choices=JENIS_NILAI_CHOICES)
    nilai = models.DecimalField(max_digits=5, decimal_places=2)
    tanggal = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Nilai"
        verbose_name_plural = "Nilai"

    def __str__(self):
        return f"Nilai {self.jenis_nilai} - {self.mata_pelajaran} - {self.siswa.nama_lengkap}"


class Raport(models.Model):
    SEMESTER_CHOICES = [('Ganjil', 'Ganjil'), ('Genap', 'Genap')]
    
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='raport')
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='Ganjil')
    catatan_wali_kelas = models.TextField(blank=True, null=True)
    izin = models.PositiveIntegerField(default=0)
    sakit = models.PositiveIntegerField(default=0)
    alpa = models.PositiveIntegerField(default=0)
    rata_rata = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Rata-rata nilai keseluruhan")
    status_naik_kelas = models.BooleanField(default=True, help_text="Centang jika naik kelas / lulus")

    class Meta:
        verbose_name = "Raport"
        verbose_name_plural = "Raport"
        unique_together = ('siswa', 'kelas', 'semester')

    def __str__(self):
        return f"Raport {self.siswa.nama_lengkap} - {self.kelas.nama_kelas} ({self.semester})"

class DetailRaport(models.Model):
    raport = models.ForeignKey(Raport, on_delete=models.CASCADE, related_name='detail_nilai')
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    nilai_akhir = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Detail Nilai Raport"
        verbose_name_plural = "Detail Nilai Raport"
        unique_together = ('raport', 'mata_pelajaran')
        
    def __str__(self):
        return f"{self.mata_pelajaran.nama_mapel} - {self.nilai_akhir}"
