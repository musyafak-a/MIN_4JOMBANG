import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdms.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Guru
from akademik.models import MataPelajaran

def run():
    print("Membuat data guru mata pelajaran...")
    
    data_guru_mapel = [
        {"nip": "198101012010011001", "nama": "M. Yasin, S.Ag", "mapel": ["AQD", "FQH"]},
        {"nip": "198202022010011002", "nama": "Hj. Umi Kulsum, M.Pd.I", "mapel": ["QH", "SKI"]},
        {"nip": "198303032010011003", "nama": "Ahmad Muzakki, Lc", "mapel": ["B.AR"]},
        {"nip": "198404042010011004", "nama": "Drs. Budi Haryanto", "mapel": ["MTK", "IPA"]},
        {"nip": "198505052010011005", "nama": "Siti Nurhaliza, S.Pd", "mapel": ["B.ID", "PPKN"]},
        {"nip": "198606062010011006", "nama": "Teguh Prakoso, S.Pd", "mapel": ["IPS"]},
        {"nip": "198707072010011007", "nama": "Dewi Sartika, S.Sn", "mapel": ["SBDP"]},
        {"nip": "198808082010011008", "nama": "John Thor, S.Pd (Sir John)", "mapel": ["BING"]},
    ]
    
    for dg in data_guru_mapel:
        # Buat user
        user, _ = User.objects.get_or_create(username=dg['nip'], defaults={'first_name': dg['nama'].split()[0]})
        user.set_password('guru123')
        user.save()
        
        # Buat profil guru
        guru, _ = Guru.objects.get_or_create(
            nip=dg['nip'],
            defaults={
                'user': user,
                'nama_lengkap': dg['nama'],
                'posisi': 'Guru Mata Pelajaran',
                'jenis_kelamin': 'L' if 'M.' in dg['nama'] or 'Ahmad' in dg['nama'] or 'Budi' in dg['nama'] or 'Teguh' in dg['nama'] or 'John' in dg['nama'] else 'P',
                'no_telepon': f"081{random.randint(10000000, 99999999)}",
                'alamat': 'Jombang'
            }
        )
        print(f"Guru {guru.nama_lengkap} dibuat.")
        
        # Assign ke mapel
        for kode in dg['mapel']:
            mapel = MataPelajaran.objects.filter(kode_mapel=kode).first()
            if mapel:
                mapel.guru_pengampu = guru
                mapel.save()
                print(f" -> Ditugaskan mengampu: {mapel.nama_mapel}")

    print("Semua data guru mata pelajaran selesai ditambahkan dan ditugaskan!")

if __name__ == '__main__':
    run()
