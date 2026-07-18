import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdms.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Siswa
from akademik.models import Kelas, TahunAjaran

def run():
    print("Menghapus data siswa yang namanya ada gelar...")
    Siswa.objects.all().delete()
    
    # Hapus juga akun usernya (yang bukan staff)
    User.objects.filter(is_staff=False, is_superuser=False).delete()
    print("Siswa lama berhasil dihapus")
    
    # Buat kelas 1A sampai 6D jika belum ada
    tahun_ajaran = TahunAjaran.objects.first()
    
    tingkatan = [1, 2, 3, 4, 5, 6]
    abjad = ['A', 'B', 'C', 'D']
    
    for t in tingkatan:
        for a in abjad:
            nama_kelas = f"{t}{a}"
            Kelas.objects.get_or_create(
                nama_kelas=nama_kelas,
                defaults={
                    'tingkat': t,
                    'tahun_ajaran': tahun_ajaran
                }
            )
    print("Kelas 1A sampai 6D sudah siap!")

if __name__ == '__main__':
    run()
