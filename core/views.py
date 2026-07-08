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


def direktori_prestasi(request):
    profile = SchoolProfile.objects.first()
    
    # Dummy data for prestasi
    dummy_prestasi = [
        {"no": 1, "tanggal": "07/07/2026", "nama": "MUTIARA FATMA KHOLIFATUN N...", "juara": "JUARA 2", "kejuaraan": "KOMPETISI ANAK CERDAS DAN BERPRESTASI", "tingkat": "-"},
        {"no": 2, "tanggal": "17/06/2026", "nama": "YOFI ANDARISTA", "juara": "JUARA 3", "kejuaraan": "TES KEMAMPUAN AKADEMIK (TKA)", "tingkat": "KABUPATEN"},
        {"no": 3, "tanggal": "07/06/2026", "nama": "AISYAH SYAKILA ANJANIA ALIF", "juara": "JUARA 2", "kejuaraan": "KSATRIA NUSANTARA SERIES CHAMPION 2026", "tingkat": "PROVINSI"},
        {"no": 4, "tanggal": "17/05/2026", "nama": "ZAURA DEANDRA CALLYSTA", "juara": "JUARA HARAPAN 2", "kejuaraan": "KOMPETISI ANAK CERDAS DAN BERPRESTASI", "tingkat": "KABUPATEN"},
        {"no": 5, "tanggal": "17/05/2026", "nama": "MUTIARA FATMA KHOLIFATUN N...", "juara": "JUARA 2", "kejuaraan": "KOMPETISI ANAK CERDAS DAN BERPRESTASI", "tingkat": "KABUPATEN"},
        {"no": 6, "tanggal": "09/05/2026", "nama": "ROSEVIONA CLARISSA HERMAN", "juara": "JUARA 1", "kejuaraan": "TAHFIDZ", "tingkat": "PROVINSI"},
        {"no": 7, "tanggal": "03/05/2026", "nama": "MUTIARA FATMA KHOLIFATUN N...", "juara": "JUARA HARAPAN 3", "kejuaraan": "LOMBA BAHASA INGGRIS FESTIVAL HARI PENDIDIKAN NASIONAL", "tingkat": "KABUPATEN"},
        {"no": 8, "tanggal": "26/04/2026", "nama": "MUTIARA FATMA KHOLIFATUN N...", "juara": "JUARA 1", "kejuaraan": "ENGLISH LEVEL 2", "tingkat": "PROVINSI"},
        {"no": 9, "tanggal": "20/04/2026", "nama": "FAKHIRAH RAMADHANI AL - IKH...", "juara": "JUARA 1", "kejuaraan": "PERINGKAT TERTINGGI NILAI TKA 2026", "tingkat": "KABUPATEN"},
        {"no": 10, "tanggal": "12/04/2026", "nama": "FAKHIRAH RAMADHANI AL IKHW...", "juara": "JUARA HARAPAN 2", "kejuaraan": "CENDEKIA SCIENCE FEST", "tingkat": "KABUPATEN"},
    ]
    
    context = {
        "profile": profile,
        "prestasi_list": dummy_prestasi,
    }
    return render(request, "core/direktori_prestasi.html", context)


def direktori_dokumen(request):
    profile = SchoolProfile.objects.first()
    
    # Dummy data for dokumen (Grouped by Category)
    data_berkas = [
        {"no": 1, "tanggal": "08/03/2026", "nama_berkas": "PIAGAM ADIWIYATA MANDIRI"},
        {"no": 2, "tanggal": "07/03/2026", "nama_berkas": "PIAGAM ADIWIYATA NASIONAL"},
        {"no": 3, "tanggal": "06/03/2026", "nama_berkas": "PIAGAM AKREDITASI 2022"},
        {"no": 4, "tanggal": "05/03/2026", "nama_berkas": "SK KEPALA MADRASAH"},
        {"no": 5, "tanggal": "04/03/2026", "nama_berkas": "NSM RESMI MADRASAH"},
        {"no": 6, "tanggal": "03/03/2026", "nama_berkas": "NPSN RESMI MADRASAH"},
        {"no": 7, "tanggal": "02/03/2026", "nama_berkas": "SERTIFIKAT TANAH MADRASAH"},
    ]
    data_profil = [
        {"no": 1, "tanggal": "03/03/2026", "nama_berkas": "STRUKTUR PPID"},
        {"no": 2, "tanggal": "02/03/2026", "nama_berkas": "VISI DAN MISI PPID"},
        {"no": 3, "tanggal": "01/03/2026", "nama_berkas": "MAKLUMAT PELAYANAN"},
    ]
    data_rekap = [
        {"no": 1, "tanggal": "23/06/2026", "nama_berkas": "REKAPITULASI PESERTA DIDIK TAHUN PELAJARAN 2025-2026 SEMESTER II"},
        {"no": 2, "tanggal": "10/04/2026", "nama_berkas": "REKAPITULASI GURU MIN 4 JOMBANG SEMESTER GENAP 2026 PER 10 APRIL 2026"},
        {"no": 3, "tanggal": "10/04/2026", "nama_berkas": "DATA GURU MIN 4 JOMBANG SEMESTER GENAP 2026 PER 10 APRIL 2026"},
        {"no": 4, "tanggal": "10/04/2026", "nama_berkas": "REKAPITULASI SISWA SEMESTER GENAP PER 10 APRIL 2026"},
        {"no": 5, "tanggal": "10/04/2026", "nama_berkas": "DATA SISWA SEMESTER GENAP PER 10 APRIL 2026"},
        {"no": 6, "tanggal": "30/12/2025", "nama_berkas": "BAP_2025_2026_GANJIL_111135170004"},
        {"no": 7, "tanggal": "05/11/2025", "nama_berkas": "EVALUASI DIRI MADRASAH 2025"},
    ]
    data_regulasi = [
        {"no": 1, "tanggal": "20/11/2025", "nama_berkas": "KEPUTUSAN MENTERI AGAMA REPUBLIK INDONESIA NOMOR 92 TAHUN 2019 TENTANG PEDOMAN LAYANAN INFORMASI PUBLIK"},
        {"no": 2, "tanggal": "20/11/2025", "nama_berkas": "KEPUTUSAN MENTERI AGAMA REPUBLIK INDONESIA NOMOR 657 TAHUN 2021 TENTANG PEJABAT PENGELOLA INFORMASI DAN DOKUMENTASI KEMENTERIAN AGAMA"},
        {"no": 3, "tanggal": "20/11/2025", "nama_berkas": "RANCANGAN MENTERI AGAMA RI TENTANG PEJABAT PENGELOLA INFORMASI DAN DOKUMENTASI KEMENTERIAN AGAMA"},
        {"no": 4, "tanggal": "20/11/2025", "nama_berkas": "RANCANGAN MENTERI AGAMA RI TENTANG PEDOMAN LAYANAN INFORMASI PUBLIK"},
        {"no": 5, "tanggal": "19/11/2025", "nama_berkas": "PERATURAN MAHKAMAH AGUNG REPUBLIK INDONESIA NOMOR :02 TAHUN 2011 TENTANG TATA CARA PENYELESAIAN SENGKETA INFORMASI PUBLIK"},
        {"no": 6, "tanggal": "18/11/2025", "nama_berkas": "PERATURAN KOMISI INFORMASI NOMOR 1 TAHUN 2013 TENTANG PROSEDUR PENYELESAIAN SENGKETA INFORMASI PUBLIK"},
        {"no": 7, "tanggal": "17/11/2025", "nama_berkas": "PERATURAN KOMISI INFORMASI REPUBLIK INDONESIA NOMOR 1 TAHUN 2021 TENTANG STANDAR LAYANAN INFORMASI PUBLIK"},
    ]
    data_sk = [
        {"no": 1, "tanggal": "02/06/2026", "nama_berkas": "SURAT KEPUTUSAN KELULUSAN PESERTA DIDIK TAHUN PELAJARAN 2025/2026"},
        {"no": 2, "tanggal": "02/05/2026", "nama_berkas": "SK KRITERIA KELULUSAN 2026"},
        {"no": 3, "tanggal": "03/03/2026", "nama_berkas": "SK PANITIA PONDOK RAMADHAN 1447 H"},
        {"no": 4, "tanggal": "31/01/2026", "nama_berkas": "SK TIM PENGELOLA SP4N- LAPOR!"},
        {"no": 5, "tanggal": "19/01/2026", "nama_berkas": "SK TIM MBG MADRASAH"},
    ]
    
    context = {
        "profile": profile,
        "data_berkas": data_berkas,
        "data_profil": data_profil,
        "data_rekap": data_rekap,
        "data_regulasi": data_regulasi,
        "data_sk": data_sk,
    }
    return render(request, "core/direktori_dokumen.html", context)
