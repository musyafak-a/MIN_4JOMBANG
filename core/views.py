from itertools import groupby
from operator import attrgetter

from django.shortcuts import render
from .models import (
    SchoolProfile, CarouselSlide, Achievement,
    OverviewStat, GalleryPhoto, Partnership,
)


def home(request):
    profile = SchoolProfile.objects.first()
    slides = CarouselSlide.objects.filter(aktif=True)
    achievements = Achievement.objects.all()
    total_prestasi = sum(a.jumlah_prestasi for a in achievements)

    stats_qs = OverviewStat.objects.all()
    overview_grouped = {
        tipe: list(items)
        for tipe, items in groupby(stats_qs, key=attrgetter("tipe"))
    }

    gallery = GalleryPhoto.objects.filter(tampilkan_di_beranda=True)[:8]
    partners = Partnership.objects.all()

    context = {
        "profile": profile,
        "slides": slides,
        "achievements": achievements,
        "total_prestasi": total_prestasi,
        "overview_grouped": overview_grouped,
        "gallery": gallery,
        "partners": partners,
    }
    return render(request, "core/home.html", context)


def sejarah(request):
    profile = SchoolProfile.objects.first()
    context = {
        "profile": profile,
    }
    return render(request, "core/sejarah.html", context)


def visi_misi(request):
    profile = SchoolProfile.objects.first()
    context = {
        "profile": profile,
    }
    return render(request, "core/visi_misi.html", context)


def struktur(request):
    profile = SchoolProfile.objects.first()
    context = {
        "profile": profile,
    }
    return render(request, "core/struktur.html", context)


def direktori_siswa(request):
    profile = SchoolProfile.objects.first()
    
    # Dummy data to match the mockup exactly
    dummy_siswa = [
        {"nama": "ABDU RABBIL ARSYL ADZIM", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "18-08-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250001"},
        {"nama": "AFKAR NURDIANSYAH PRADIPTA", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "08-12-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250002"},
        {"nama": "AHMAD HILMI RIZA", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "12-01-2019", "jk": "LAKI - LAKI", "nis": "1111951700806250003"},
        {"nama": "AHMAD JALALUDDIN AL GHAZALI", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "05-10-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250004"},
        {"nama": "AHMAD WIDE WIRARAJA", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Lumajang", "tgl_lahir": "31-12-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250005"},
        {"nama": "ALFIYAH AHSANUL MAIDAH", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "10-08-2018", "jk": "PEREMPUAN", "nis": "1111951700806250006"},
        {"nama": "ALVIN ZAIDAN FAEYZA", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "03-03-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250007"},
        {"nama": "ARSYA DWI PUTRA ALFAHRIZA", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "17-05-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250008"},
        {"nama": "AZKADINA KANZIA NADHIFAH NUR HAFI", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Kediri", "tgl_lahir": "20-02-2019", "jk": "PEREMPUAN", "nis": "1111951700806250009"},
        {"nama": "CINTYA SHABIRA GEMINTANG", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "06-09-2018", "jk": "PEREMPUAN", "nis": "1111951700806250010"},
        {"nama": "FANDHI HAFIZ ALFARABI", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Kudus", "tgl_lahir": "20-08-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250011"},
        {"nama": "FAWWAZ DZAKI ARRAYYAN", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "13-11-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250012"},
        {"nama": "FEBBY DWI WAHYUNI", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "27-02-2019", "jk": "PEREMPUAN", "nis": "1111951700806250013"},
        {"nama": "GILBY NAUFAL DHAFIN", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jakarta", "tgl_lahir": "28-04-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250014"},
        {"nama": "HAMIZAN HAQQI EL-HASAN", "kelas": "3 - AR RAHMAN", "tempat_lahir": "Jombang", "tgl_lahir": "01-07-2018", "jk": "LAKI - LAKI", "nis": "1111951700806250015"},
    ]
    
    context = {
        "profile": profile,
        "siswa_list": dummy_siswa,
    }
    return render(request, "core/direktori_siswa.html", context)


def direktori_alumni(request):
    profile = SchoolProfile.objects.first()
    
    # Dummy data for alumni
    dummy_alumni = [
        {"nama": "ABDUL ROSYID AL HAFIDZH", "tahun_lulus": "2025/2026", "tempat_lahir": "Jombang", "tgl_lahir": "06-02-2014", "jk": "LAKI - LAKI", "foto": "https://placehold.co/400x400/255F38/FFFFFF?text=Foto+Siswa"},
        {"nama": "NUR LAILA FITRIANI", "tahun_lulus": "2024/2025", "tempat_lahir": "Surabaya", "tgl_lahir": "12-08-2013", "jk": "PEREMPUAN", "foto": "https://placehold.co/400x400/255F38/FFFFFF?text=Foto+Siswi"},
        {"nama": "MUHAMMAD FARHAN", "tahun_lulus": "2025/2026", "tempat_lahir": "Sidoarjo", "tgl_lahir": "20-11-2014", "jk": "LAKI - LAKI", "foto": "https://placehold.co/400x400/255F38/FFFFFF?text=Foto+Siswa"},
        {"nama": "SITI AMINAH", "tahun_lulus": "2023/2024", "tempat_lahir": "Jombang", "tgl_lahir": "05-04-2012", "jk": "PEREMPUAN", "foto": "https://placehold.co/400x400/255F38/FFFFFF?text=Foto+Siswi"},
        {"nama": "AHMAD ZAKARIA", "tahun_lulus": "2025/2026", "tempat_lahir": "Mojokerto", "tgl_lahir": "15-01-2014", "jk": "LAKI - LAKI", "foto": "https://placehold.co/400x400/255F38/FFFFFF?text=Foto+Siswa"},
        {"nama": "INTAN PERMATASARI", "tahun_lulus": "2024/2025", "tempat_lahir": "Jombang", "tgl_lahir": "28-09-2013", "jk": "PEREMPUAN", "foto": "https://placehold.co/400x400/255F38/FFFFFF?text=Foto+Siswi"},
        {"nama": "REZA WAHYUDI", "tahun_lulus": "2023/2024", "tempat_lahir": "Kediri", "tgl_lahir": "10-12-2012", "jk": "LAKI - LAKI", "foto": "https://placehold.co/400x400/255F38/FFFFFF?text=Foto+Siswa"},
        {"nama": "DINA MARIANA", "tahun_lulus": "2025/2026", "tempat_lahir": "Jombang", "tgl_lahir": "17-06-2014", "jk": "PEREMPUAN", "foto": "https://placehold.co/400x400/255F38/FFFFFF?text=Foto+Siswi"},
    ]
    
    context = {
        "profile": profile,
        "alumni_list": dummy_alumni,
    }
    return render(request, "core/direktori_alumni.html", context)
