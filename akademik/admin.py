from django.contrib import admin
from .models import TahunAjaran, Kelas, SiswaKelas, MataPelajaran, Nilai, Raport, DetailRaport

class SiswaKelasInline(admin.TabularInline):
    model = SiswaKelas
    extra = 1

class DetailRaportInline(admin.TabularInline):
    model = DetailRaport
    extra = 5

@admin.register(TahunAjaran)
class TahunAjaranAdmin(admin.ModelAdmin):
    list_display = ('nama', 'semester', 'is_active')
    list_filter = ('semester', 'is_active')

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama_kelas', 'tingkat', 'wali_kelas', 'tahun_ajaran')
    list_filter = ('tingkat', 'tahun_ajaran')
    search_fields = ('nama_kelas',)
    inlines = [SiswaKelasInline]

@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('kode_mapel', 'nama_mapel')
    search_fields = ('kode_mapel', 'nama_mapel')

@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'mata_pelajaran', 'kelas', 'jenis_nilai', 'nilai')
    list_filter = ('jenis_nilai', 'kelas', 'mata_pelajaran')
    search_fields = ('siswa__nama_lengkap',)

@admin.register(Raport)
class RaportAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'kelas', 'semester', 'rata_rata', 'status_naik_kelas')
    list_filter = ('kelas', 'semester', 'status_naik_kelas')
    search_fields = ('siswa__nama_lengkap',)
    inlines = [DetailRaportInline]
