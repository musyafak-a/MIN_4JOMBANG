import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdms.settings')
django.setup()

from django.contrib.auth.models import User, Group
from accounts.models import Siswa
from akademik.models import Kelas, SiswaKelas, MataPelajaran, Nilai, Raport, DetailRaport

try:
    from faker import Faker
    fake = Faker('id_ID')
except ImportError:
    print("Faker belum terinstall. Script ini butuh faker.")
    exit()

def run():
    print("Mulai membuat data dummy massal...")
    
    # Ambil semua kelas
    semua_kelas = Kelas.objects.all()
    if not semua_kelas:
        print("Belum ada kelas yang terdaftar. Buat kelas terlebih dahulu.")
        return
        
    semua_mapel = MataPelajaran.objects.all()
    
    # Kita asumsikan kita ingin setiap kelas memiliki 25 siswa
    TARGET_SISWA_PER_KELAS = 25
    nisn_counter = 1110000
    
    for kelas in semua_kelas:
        siswa_saat_ini = SiswaKelas.objects.filter(kelas=kelas).count()
        kekurangan = TARGET_SISWA_PER_KELAS - siswa_saat_ini
        
        if kekurangan <= 0:
            print(f"Kelas {kelas.nama_kelas} sudah memiliki >= 25 siswa.")
            continue
            
        print(f"Menambahkan {kekurangan} siswa ke {kelas.nama_kelas}...")
        
        for _ in range(kekurangan):
            # Generate Data Siswa
            nisn = str(nisn_counter + random.randint(1, 999999))
            nisn_counter += 1
            
            jenis_kelamin = random.choice(['L', 'P'])
            if jenis_kelamin == 'L':
                nama_lengkap = f"{fake.first_name_male()} {fake.last_name_male()}"
            else:
                nama_lengkap = f"{fake.first_name_female()} {fake.last_name_female()}"
                
            # Buat User login
            user, created = User.objects.get_or_create(username=nisn)
            if created:
                user.set_password("siswa123")
                user.save()
                
            # Buat profil Siswa
            siswa, _ = Siswa.objects.get_or_create(
                user=user,
                defaults={
                    'nisn': nisn,
                    'nis': str(int(nisn) - 100000), # NIS berbeda dari NISN
                    'nama_lengkap': nama_lengkap,
                    'tempat_lahir': fake.city(),
                    'tanggal_lahir': fake.date_of_birth(minimum_age=6, maximum_age=12),
                    'jenis_kelamin': jenis_kelamin,
                    'alamat': fake.address()
                }
            )
            
            # Daftarkan ke kelas
            SiswaKelas.objects.get_or_create(
                siswa=siswa,
                kelas=kelas
            )
            
            # Generate Nilai Acak untuk beberapa mapel
            for mapel in semua_mapel:
                # Tugas
                Nilai.objects.get_or_create(siswa=siswa, mata_pelajaran=mapel, kelas=kelas, jenis_nilai='Tugas', defaults={'nilai': Decimal(random.randint(70, 100))})
                # UH 1
                Nilai.objects.get_or_create(siswa=siswa, mata_pelajaran=mapel, kelas=kelas, jenis_nilai='Ulangan Harian 1', defaults={'nilai': Decimal(random.randint(65, 100))})
                # UTS
                Nilai.objects.get_or_create(siswa=siswa, mata_pelajaran=mapel, kelas=kelas, jenis_nilai='UTS', defaults={'nilai': Decimal(random.randint(70, 100))})
                # UAS
                Nilai.objects.get_or_create(siswa=siswa, mata_pelajaran=mapel, kelas=kelas, jenis_nilai='UAS', defaults={'nilai': Decimal(random.randint(65, 100))})

            # Generate Raport
            raport, _ = Raport.objects.get_or_create(
                siswa=siswa,
                kelas=kelas,
                semester='Ganjil',
                defaults={
                    'izin': random.randint(0, 3),
                    'sakit': random.randint(0, 5),
                    'alpa': random.randint(0, 1),
                    'catatan_wali_kelas': fake.sentence()
                }
            )
            
            # Hitung rata-rata dan detail raport
            total_nilai = 0
            count_mapel = len(semua_mapel)
            
            for mapel in semua_mapel:
                nilai_akhir = Decimal(random.randint(75, 100))
                total_nilai += nilai_akhir
                DetailRaport.objects.get_or_create(
                    raport=raport,
                    mata_pelajaran=mapel,
                    defaults={'nilai_akhir': nilai_akhir}
                )
                
            if count_mapel > 0:
                raport.rata_rata = total_nilai / count_mapel
                raport.save()

    print("Selesai! Semua kelas sekarang penuh dengan siswa dan nilai acak.")

if __name__ == '__main__':
    run()
