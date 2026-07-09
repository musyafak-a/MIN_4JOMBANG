import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdms.settings')
django.setup()

from akademik.models import MataPelajaran

def run():
    print("Menambahkan mata pelajaran baru...")
    mapel_baru = [
        {'nama': 'PPKn', 'kode': 'PPKN', 'tingkat': 1},
        {'nama': 'Ilmu Pengetahuan Sosial', 'kode': 'IPS', 'tingkat': 1},
        {'nama': 'Seni Budaya', 'kode': 'SBDP', 'tingkat': 1},
        {'nama': 'Bahasa Inggris', 'kode': 'BING', 'tingkat': 2}, # Bahasa inggris mulai kelas 2
    ]
    
    for m in mapel_baru:
        MataPelajaran.objects.get_or_create(
            kode_mapel=m['kode'],
            defaults={
                'nama_mapel': m['nama'],
                'tingkat_minimal': m['tingkat']
            }
        )
    print("Mata pelajaran PPKn, IPS, SBDP, dan B. Inggris (mulai kelas 2) berhasil ditambahkan.")

if __name__ == '__main__':
    run()
