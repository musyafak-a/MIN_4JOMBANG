from django.urls import path
from . import views

app_name = 'admin_sekolah_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Kelola Berita
    path('berita/', views.kelola_berita, name='kelola_berita'),
    path('berita/tambah/', views.form_berita, name='tambah_berita'),
    path('berita/edit/<int:id>/', views.form_berita, name='edit_berita'),
    path('berita/hapus/<int:id>/', views.hapus_berita, name='hapus_berita'),
    
    # Kelola Pengumuman
    path('pengumuman/', views.kelola_pengumuman, name='kelola_pengumuman'),
    path('pengumuman/tambah/', views.form_pengumuman, name='tambah_pengumuman'),
    path('pengumuman/edit/<int:id>/', views.form_pengumuman, name='edit_pengumuman'),
    path('pengumuman/hapus/<int:id>/', views.hapus_pengumuman, name='hapus_pengumuman'),
]
