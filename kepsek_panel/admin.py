from django.contrib import admin
from .models import PersetujuanCuti, PersetujuanAnggaran, TandaTanganRaport, LaporanPPDB, LaporanMutasi, LaporanKelulusan

@admin.register(PersetujuanCuti)
class PersetujuanCutiAdmin(admin.ModelAdmin):
    list_display = ('guru', 'tanggal_mulai', 'tanggal_selesai', 'status')
    list_filter = ('status',)
    search_fields = ('guru__nama_lengkap',)

@admin.register(PersetujuanAnggaran)
class PersetujuanAnggaranAdmin(admin.ModelAdmin):
    list_display = ('judul', 'pengaju', 'jumlah', 'status')
    list_filter = ('status',)
    search_fields = ('judul', 'pengaju__nama_lengkap')

@admin.register(TandaTanganRaport)
class TandaTanganRaportAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'kelas', 'semester', 'is_signed_by_kepsek')
    list_filter = ('is_signed_by_kepsek', 'kelas', 'semester')
    search_fields = ('siswa__nama_lengkap',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_signed_by_kepsek=False)

@admin.register(LaporanPPDB)
class LaporanPPDBAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'asal_sekolah', 'tanggal_daftar', 'status_diterima')
    list_filter = ('status_diterima',)
    search_fields = ('nama_lengkap', 'asal_sekolah')

@admin.register(LaporanMutasi)
class LaporanMutasiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'jenis_mutasi', 'tanggal', 'keterangan_sekolah')
    list_filter = ('jenis_mutasi',)
    search_fields = ('siswa__nama_lengkap',)

@admin.register(LaporanKelulusan)
class LaporanKelulusanAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'kelas', 'rata_rata', 'status_naik_kelas')
    list_filter = ('kelas', 'status_naik_kelas')
    search_fields = ('siswa__nama_lengkap',)

    def get_queryset(self, request):
        # Lulus = tingkat 6, status_naik_kelas = True
        return super().get_queryset(request).filter(kelas__tingkat='6', status_naik_kelas=True)
