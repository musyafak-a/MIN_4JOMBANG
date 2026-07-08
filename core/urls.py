from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("sejarah/", views.sejarah, name="sejarah"),
    path("visi-misi/", views.visi_misi, name="visi_misi"),
    path("struktur/", views.struktur, name="struktur"),
]
