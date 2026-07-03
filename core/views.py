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
