import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdms.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import Guru, Siswa
from akademik.models import TahunAjaran, Kelas, SiswaKelas, MataPelajaran, Nilai, Raport
from core.models import Berita, Alumni, Achievement, OverviewStat, GalleryPhoto, Partnership, CarouselSlide, SchoolProfile

def run():
    print("Mengatur hak akses (permissions)...")
    
    # Buat Group "Guru"
    guru_group, created = Group.objects.get_or_create(name='Guru')
    
    # Tentukan model-model yang boleh diakses oleh Guru biasa
    models_to_grant = [
        Siswa, TahunAjaran, Kelas, SiswaKelas, MataPelajaran, Nilai, Raport
    ]
    
    # Tambahkan semua permission (add, change, delete, view) untuk model-model di atas ke Group Guru
    for model in models_to_grant:
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        for perm in permissions:
            guru_group.permissions.add(perm)
            
    # Masukkan semua akun user yang tertaut ke profil Guru ke dalam Group "Guru"
    semua_guru = Guru.objects.all()
    for g in semua_guru:
        g.user.groups.add(guru_group)
        
    print("✅ Hak akses berhasil diberikan ke semua Guru!")

if __name__ == '__main__':
    run()
