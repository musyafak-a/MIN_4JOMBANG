from django.contrib import admin
from .models import (
    SchoolProfile, CarouselSlide, Achievement,
    OverviewStat, GalleryPhoto, Partnership,
)


@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = ("nama_sekolah", "tahun_berdiri")
    list_per_page = 10

    def has_add_permission(self, request):
        # Singleton: cegah admin bikin lebih dari 1 profil
        return not SchoolProfile.objects.exists()


@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ("judul", "urutan", "aktif")
    list_editable = ("urutan", "aktif")
    ordering = ("urutan",)
    list_per_page = 10


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("bidang", "kategori", "jumlah_prestasi", "tingkat_tertinggi", "urutan")
    list_editable = ("urutan",)
    list_filter = ("kategori",)
    list_per_page = 10


@admin.register(OverviewStat)
class OverviewStatAdmin(admin.ModelAdmin):
    list_display = ("tipe", "label", "nilai", "urutan")
    list_editable = ("nilai", "urutan")
    list_filter = ("tipe",)
    list_per_page = 10


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ("judul", "kategori", "tanggal", "tampilkan_di_beranda", "urutan")
    list_editable = ("urutan", "tampilkan_di_beranda")
    list_filter = ("kategori",)
    list_per_page = 10


@admin.register(Partnership)
class PartnershipAdmin(admin.ModelAdmin):
    list_display = ("nama", "urutan")
    list_editable = ("urutan",)
    list_per_page = 10

from .models import Berita, Alumni

@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ("judul", "penulis", "tanggal_publikasi", "status")
    list_filter = ("status", "tanggal_publikasi")
    search_fields = ("judul",)
    prepopulated_fields = {"slug": ("judul",)}
    list_per_page = 10

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ("nama", "tahun_lulus", "pekerjaan_sekarang")
    list_filter = ("tahun_lulus",)
    search_fields = ("nama", "pekerjaan_sekarang")
    list_per_page = 10

