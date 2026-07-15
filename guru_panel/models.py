from django.db import models
from accounts.models import Guru

class CutiGuru(models.Model):
    STATUS_CHOICES = [
        ('Menunggu', 'Menunggu'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
    ]
    
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, related_name='pengajuan_cuti')
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    alasan = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Menunggu')
    tanggal_pengajuan = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cuti Guru/Staf"
        verbose_name_plural = "Cuti Guru/Staf"

    def __str__(self):
        return f"Cuti {self.guru.nama_lengkap} ({self.tanggal_mulai} - {self.tanggal_selesai})"

class PengajuanAnggaran(models.Model):
    STATUS_CHOICES = [
        ('Menunggu', 'Menunggu'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
    ]
    
    pengaju = models.ForeignKey(Guru, on_delete=models.CASCADE, related_name='pengajuan_anggaran')
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    file_proposal = models.FileField(upload_to='proposal_anggaran/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Menunggu')
    tanggal_pengajuan = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pengajuan Anggaran"
        verbose_name_plural = "Pengajuan Anggaran"

    def __str__(self):
        return f"{self.judul} - {self.pengaju.nama_lengkap}"
