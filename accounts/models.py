from django.db import models
from django.contrib.auth.models import User

class Guru(models.Model):
    POSISI_CHOICES = [
        ('Kepala Sekolah', 'Kepala Sekolah'),
        ('Guru Kelas', 'Guru Kelas'),
        ('Guru Mata Pelajaran', 'Guru Mata Pelajaran'),
        ('Staf', 'Staf'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_guru')
    nip = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIP")
    nama_lengkap = models.CharField(max_length=150)
    posisi = models.CharField(max_length=50, choices=POSISI_CHOICES, default='Guru Kelas')
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    no_telepon = models.CharField(max_length=15, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='foto_guru/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Guru"
        verbose_name_plural = "Guru"
        
    def __str__(self):
        return f"{self.nama_lengkap} ({self.posisi})"

    def save(self, *args, **kwargs):
        # Logika untuk menjadikan Kepala Sekolah sebagai superuser
        is_kepsek = (self.posisi == 'Kepala Sekolah')
        
        # Simpan profil Guru terlebih dahulu untuk mendapatkan user, 
        # namun kita juga bisa update usernya
        super().save(*args, **kwargs)
        
        # Semua guru bisa login ke admin (is_staff = True)
        # Hanya Kepala Sekolah yang jadi superuser (is_superuser = True)
        self.user.is_staff = True
        self.user.is_superuser = is_kepsek
        self.user.save()


class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_siswa', help_text="Akun untuk siswa (opsional)")
    nisn = models.CharField(max_length=50, unique=True, verbose_name="NISN")
    nis = models.CharField(max_length=50, unique=True, verbose_name="NIS")
    nama_lengkap = models.CharField(max_length=150)
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    nama_ayah = models.CharField(max_length=150, blank=True, null=True)
    nama_ibu = models.CharField(max_length=150, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='foto_siswa/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Siswa"
        verbose_name_plural = "Siswa"
        
    def __str__(self):
        return self.nama_lengkap
