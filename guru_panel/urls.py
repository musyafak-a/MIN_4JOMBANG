from django.urls import path
from . import views

app_name = 'guru_panel'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('siswa/', views.siswa_view, name='siswa'),
    path('kelas/', views.kelas_view, name='kelas'),
    path('nilai/', views.nilai_view, name='nilai'),
    path('raport/', views.raport_view, name='raport'),
    path('jadwal/', views.jadwal_view, name='jadwal'),
]
