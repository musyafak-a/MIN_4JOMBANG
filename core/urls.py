from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("sejarah/", views.sejarah, name="sejarah"),
    path("visi-misi/", views.visi_misi, name="visi_misi"),
    path("struktur/", views.struktur, name="struktur"),
    path("direktori/siswa/", views.direktori_siswa, name="direktori_siswa"),
    path("direktori/alumni/", views.direktori_alumni, name="direktori_alumni"),
    path("direktori/prestasi/", views.direktori_prestasi, name="direktori_prestasi"),
    path("direktori/dokumen/", views.direktori_dokumen, name="direktori_dokumen"),
]
