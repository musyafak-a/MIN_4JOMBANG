import os
import django
from datetime import date

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdms.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Guru, Siswa
from akademik.models import TahunAjaran, Kelas, SiswaKelas, MataPelajaran, Nilai, Raport
from core.models import Berita, Alumni

def run():
    print("Menghapus data lama...")
    User.objects.filter(is_superuser=False).delete()
    Guru.objects.all().delete()
    Siswa.objects.all().delete()
    TahunAjaran.objects.all().delete()
    Kelas.objects.all().delete()
    MataPelajaran.objects.all().delete()
    
    print("Membuat Mata Pelajaran Madrasah (MIN)...")
    mapel_data = [
        ("AQD", "Aqidah Akhlak", "Pelajaran tentang keimanan dan akhlak terpuji"),
        ("FQH", "Fiqih", "Pelajaran tentang tata cara ibadah sehari-hari"),
        ("QH", "Al-Qur'an Hadis", "Pelajaran membaca dan memahami isi kandungan Al-Qur'an dan Hadis"),
        ("SKI", "Sejarah Kebudayaan Islam", "Pelajaran sejarah masuk dan berkembangnya Islam"),
        ("B.AR", "Bahasa Arab", "Bahasa Arab dasar untuk madrasah ibtidaiyah"),
        ("MTK", "Matematika", "Matematika dasar"),
        ("IPA", "Ilmu Pengetahuan Alam", "IPA dasar"),
        ("B.ID", "Bahasa Indonesia", "Bahasa dan Sastra Indonesia")
    ]
    mapel_objs = []
    for kode, nama, desc in mapel_data:
        mapel, _ = MataPelajaran.objects.get_or_create(kode_mapel=kode, nama_mapel=nama, deskripsi=desc)
        mapel_objs.append(mapel)
        
    print("Membuat Tahun Ajaran...")
    ta, _ = TahunAjaran.objects.get_or_create(nama="2026/2027", semester="Ganjil", is_active=True)
    
    print("Membuat User dan Profil Guru (Kepala Sekolah & Guru Kelas)...")
    # Kepala Sekolah
    user_kepsek, _ = User.objects.get_or_create(username="198001012005011001", defaults={'first_name': 'Ahmad', 'last_name': 'Dahlan'})
    user_kepsek.set_password("kepsek123") # Set password
    user_kepsek.save()
    kepsek, _ = Guru.objects.get_or_create(
        user=user_kepsek,
        nip="198001012005011001",
        nama_lengkap="H. Ahmad Dahlan, S.Pd.I, M.Pd",
        posisi="Kepala Sekolah",
        jenis_kelamin="L",
        no_telepon="081234567890",
        alamat="Jl. Pesantren No.1, Jombang"
    )
    kepsek.save() # Memicu logika superuser
    
    # Guru Kelas 1
    user_guru1, _ = User.objects.get_or_create(username="198502022010012002", defaults={'first_name': 'Siti', 'last_name': 'Aisyah'})
    user_guru1.set_password("guru123")
    user_guru1.save()
    guru1, _ = Guru.objects.get_or_create(
        user=user_guru1,
        nip="198502022010012002",
        nama_lengkap="Siti Aisyah, S.Pd.I",
        posisi="Guru Kelas",
        jenis_kelamin="P",
        no_telepon="082233445566",
        alamat="Jl. KH Hasyim Asyari, Jombang"
    )

    print("Membuat Kelas...")
    kelas1a, _ = Kelas.objects.get_or_create(tingkat="1", nama_kelas="1A", wali_kelas=guru1, tahun_ajaran=ta)
    
    print("Membuat User dan Profil Siswa...")
    siswa_data = [
        ("0123456789", "1001", "Muhammad Al-Fatih", "L", "Jombang", date(2018, 5, 12), "Budi Santoso", "Siti Aminah"),
        ("0123456790", "1002", "Fatimatuz Zahra", "P", "Mojokerto", date(2018, 8, 20), "Arif Rahman", "Lailatul Qodriyah"),
    ]
    
    siswa_objs = []
    for nisn, nis, nama, jk, tempat, tgl, ayah, ibu in siswa_data:
        # User untuk siswa login (misal username: NISN, password: NIS)
        user_siswa, _ = User.objects.get_or_create(username=nisn, defaults={'first_name': nama.split()[0]})
        user_siswa.set_password(nis) # Set password = NIS agar mudah diingat
        user_siswa.save()
        
        siswa, _ = Siswa.objects.get_or_create(
            user=user_siswa,
            nisn=nisn,
            nis=nis,
            nama_lengkap=nama,
            jenis_kelamin=jk,
            tempat_lahir=tempat,
            tanggal_lahir=tgl,
            nama_ayah=ayah,
            nama_ibu=ibu,
            alamat="Perumahan Indah, Jombang"
        )
        siswa_objs.append(siswa)
        # Masukkan ke Kelas
        SiswaKelas.objects.get_or_create(siswa=siswa, kelas=kelas1a)
        
    print("Memasukkan dummy Nilai dan Raport...")
    for siswa in siswa_objs:
        for mapel in mapel_objs[:4]: # Kasih nilai untuk 4 mapel pertama (Agama)
            Nilai.objects.get_or_create(
                siswa=siswa,
                mata_pelajaran=mapel,
                kelas=kelas1a,
                jenis_nilai="UAS",
                defaults={'nilai': 85.50}
            )
        Raport.objects.get_or_create(
            siswa=siswa,
            kelas=kelas1a,
            defaults={
                'catatan_wali_kelas': f"Ananda {siswa.nama_lengkap} sangat rajin mengaji dan disiplin, tingkatkan terus prestasinya.",
                'izin': 1,
                'sakit': 0,
                'alpa': 0,
                'status_naik_kelas': True
            }
        )

    print("Membuat Berita & Alumni dummy...")
    Berita.objects.get_or_create(
        judul="Peringatan Hari Santri Nasional 2026",
        slug="hari-santri-2026",
        konten="Seluruh siswa MIN 4 Jombang melaksanakan upacara Hari Santri dengan khidmat menggunakan busana muslim.",
        penulis=user_kepsek
    )
    Alumni.objects.get_or_create(
        nama="Ust. Hanan Attaki (Dummy)",
        tahun_lulus=2000,
        pekerjaan_sekarang="Pendakwah",
        testimoni="MIN 4 Jombang memberikan landasan agama yang sangat kuat bagi kehidupan saya."
    )
    
    print("Dummy data MIN berhasil dibuat!")


if __name__ == '__main__':
    run()
