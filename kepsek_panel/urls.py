from django.urls import path
from . import views

app_name = 'kepsek_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Persetujuan
    path('persetujuan-cuti/', views.persetujuan_cuti, name='persetujuan_cuti'),
    path('persetujuan-cuti/<int:cuti_id>/<str:action>/', views.action_cuti, name='action_cuti'),
    
    path('persetujuan-anggaran/', views.persetujuan_anggaran, name='persetujuan_anggaran'),
    path('persetujuan-anggaran/<int:anggaran_id>/<str:action>/', views.action_anggaran, name='action_anggaran'),
    
    # Tanda Tangan
    path('tanda-tangan-raport/', views.tanda_tangan_raport, name='tanda_tangan_raport'),
    path('sign-raport/<int:raport_id>/', views.sign_raport, name='sign_raport'),
    
    # Laporan
    path('laporan-ppdb/', views.laporan_ppdb, name='laporan_ppdb'),
    path('laporan-mutasi/', views.laporan_mutasi, name='laporan_mutasi'),
    path('laporan-kelulusan/', views.laporan_kelulusan, name='laporan_kelulusan'),
]
