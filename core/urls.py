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
    path("informasi/spmb/", views.spmb, name="spmb"),
    path("informasi/berita/", views.berita, name="berita"),
    path("pengumuman/", views.pengumuman, name="pengumuman"),
    path('login/', views.login_siswa, name='login_siswa'),
    path('lupa-password/', views.lupa_password, name='lupa_password'),
    path('verifikasi-otp/', views.verifikasi_otp, name='verifikasi_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('dashboard-siswa/', views.dashboard_siswa, name='dashboard_siswa'),
]
