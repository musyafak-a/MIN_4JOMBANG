from django.contrib import admin
from .models import Guru, Siswa

@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'nip', 'posisi', 'no_telepon')
    list_filter = ('posisi', 'jenis_kelamin')
    search_fields = ('nama_lengkap', 'nip', 'user__username')
    list_per_page = 10

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'nis', 'nisn', 'jenis_kelamin')
    search_fields = ('nama_lengkap', 'nis', 'nisn', 'user__username')
    list_filter = ('jenis_kelamin',)
    list_per_page = 10
