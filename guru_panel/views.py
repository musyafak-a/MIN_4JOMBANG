from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from decimal import Decimal
from accounts.models import Siswa
from akademik.models import Kelas, Nilai, Raport, MataPelajaran, Jadwal, TahunAjaran

def is_guru_user(user):
    return user.is_authenticated and (hasattr(user, 'profil_guru') or user.is_superuser or user.is_staff)

def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profil_guru'):
            if request.user.profil_guru.posisi == 'Kepala Sekolah':
                return redirect('kepsek_panel:dashboard')
            return redirect('guru_panel:dashboard')
        elif hasattr(request.user, 'profil_admin_sekolah'):
            return redirect('admin_sekolah_panel:dashboard')
        elif hasattr(request.user, 'profil_siswa'):
            return redirect('core:dashboard_siswa')
        else:
            return redirect('admin:index')
        
    if request.method == 'POST':
        nip = request.POST.get('nip') or request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=nip, password=password)
        if user is not None:
            if hasattr(user, 'profil_guru') or user.is_staff or user.is_superuser:
                login(request, user)
                if hasattr(user, 'profil_guru') and user.profil_guru.posisi == 'Kepala Sekolah':
                    return redirect('kepsek_panel:dashboard')
                return redirect('guru_panel:dashboard')
            else:
                messages.error(request, 'Akun ini bukan akun Guru atau Kepala Sekolah.')
        else:
            messages.error(request, 'NIP atau Password salah.')
            
    return render(request, 'guru_panel/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Anda telah keluar.')
    return redirect('guru_panel:login')

from django.core.paginator import Paginator

@login_required(login_url='guru_panel:login')
@user_passes_test(is_guru_user, login_url='guru_panel:login')
def dashboard_view(request):
    return render(request, 'guru_panel/dashboard.html')

@login_required(login_url='guru_panel:login')
@user_passes_test(is_guru_user, login_url='guru_panel:login')
def siswa_view(request):
    siswa_list = Siswa.objects.all().order_by('nama_lengkap')
    paginator = Paginator(siswa_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'guru_panel/siswa.html', {'page_obj': page_obj})

@login_required(login_url='guru_panel:login')
@user_passes_test(is_guru_user, login_url='guru_panel:login')
def kelas_view(request):
    kelas_list = Kelas.objects.all().select_related('wali_kelas', 'tahun_ajaran').order_by('nama_kelas')
    return render(request, 'guru_panel/kelas.html', {'kelas_list': kelas_list})

@login_required(login_url='guru_panel:login')
@user_passes_test(is_guru_user, login_url='guru_panel:login')
def nilai_view(request):
    nilai_list = Nilai.objects.all().select_related('siswa', 'kelas', 'mata_pelajaran').order_by('-tanggal')
    paginator = Paginator(nilai_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'guru_panel/nilai.html', {'page_obj': page_obj})

@login_required(login_url='guru_panel:login')
@user_passes_test(is_guru_user, login_url='guru_panel:login')
def raport_view(request):
    raport_list = Raport.objects.all().select_related('siswa', 'kelas').order_by('siswa__nama_lengkap')
    paginator = Paginator(raport_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'guru_panel/raport.html', {'page_obj': page_obj})

@login_required(login_url='guru_panel:login')
@user_passes_test(is_guru_user, login_url='guru_panel:login')
def jadwal_view(request):
    tahun_ajaran_aktif = TahunAjaran.objects.filter(is_active=True).first()
    
    suffixes = ['A', 'B', 'C', 'D']
    selected_suffix = request.GET.get('suffix', 'A')
    if selected_suffix not in suffixes:
        selected_suffix = 'A'
        
    hari_list = ['Sabtu', 'Ahad', 'Senin', 'Selasa', 'Rabu', 'Kamis']
    jam_ke_list = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    tingkat_list = list(range(1, 7))
    
    class_names = [f"{tingkat}{selected_suffix}" for tingkat in tingkat_list]
    
    jadwal_qs = Jadwal.objects.filter(
        kelas__tahun_ajaran=tahun_ajaran_aktif,
        kelas__nama_kelas__in=class_names
    ).select_related('mata_pelajaran', 'kelas', 'mata_pelajaran__guru_pengampu')
    
    jadwal_map = {}
    for j in jadwal_qs:
        tingkat = int(j.kelas.tingkat)
        jadwal_map[(j.hari, j.jam_ke, tingkat)] = j
        
    matrix_rows = []
    for hari in hari_list:
        for jam_ke in jam_ke_list:
            row_schedules = []
            for tingkat in tingkat_list:
                j = jadwal_map.get((hari, jam_ke, tingkat))
                row_schedules.append(j)
            matrix_rows.append({
                'hari': hari,
                'jam_ke': jam_ke,
                'schedules': row_schedules
            })
            
    context = {
        'tahun_ajaran_aktif': tahun_ajaran_aktif,
        'suffixes': suffixes,
        'selected_suffix': selected_suffix,
        'tingkat_list': tingkat_list,
        'matrix_rows': matrix_rows,
        'rowspan_count': len(jam_ke_list)
    }
    return render(request, 'guru_panel/jadwal.html', context)

@login_required(login_url='guru_panel:login')
@user_passes_test(is_guru_user, login_url='guru_panel:login')
def input_nilai_view(request):
    if not hasattr(request.user, 'profil_guru'):
        messages.error(request, "Hanya Guru yang dapat memasukkan nilai.")
        return redirect('core:home')
        
    guru = request.user.profil_guru
    mapel_diampu = MataPelajaran.objects.filter(guru_pengampu=guru)
    
    if not mapel_diampu.exists():
        # Tambahkan jika tidak ada di database
        mapel_default = MataPelajaran.objects.filter(nama_mapel__iexact='Bahasa Indonesia').first()
        if not mapel_default:
            mapel_default = MataPelajaran.objects.filter(guru_pengampu__isnull=True).first()
        if not mapel_default:
            mapel_default = MataPelajaran.objects.create(
                kode_mapel='B.ID', 
                nama_mapel='Bahasa Indonesia', 
                tingkat_minimal=1
            )
        mapel_default.guru_pengampu = guru
        mapel_default.save()
        mapel_diampu = MataPelajaran.objects.filter(guru_pengampu=guru)
        
    if request.method == 'POST':
        siswa_id = request.POST.get('siswa')
        kelas_id = request.POST.get('kelas')
        mapel_id = request.POST.get('mata_pelajaran')
        jenis_nilai = request.POST.get('jenis_nilai')
        nilai_val = request.POST.get('nilai')
        
        # Fallback jika select disabled di-submit kosong
        if not mapel_id and mapel_diampu.count() == 1:
            mapel_id = mapel_diampu.first().id
            
        if not (siswa_id and kelas_id and mapel_id and jenis_nilai and nilai_val):
            messages.error(request, "Semua kolom wajib diisi.")
        else:
            try:
                siswa = Siswa.objects.get(id=siswa_id)
                kelas = Kelas.objects.get(id=kelas_id)
                mapel = MataPelajaran.objects.get(id=mapel_id)
                
                # Cek hak akses guru pengampu mapel
                if mapel.guru_pengampu != guru:
                    messages.error(request, "Anda tidak berhak memasukkan nilai untuk mata pelajaran ini.")
                    return redirect('guru_panel:nilai')
                
                # Simpan Nilai
                Nilai.objects.create(
                    siswa=siswa,
                    kelas=kelas,
                    mata_pelajaran=mapel,
                    jenis_nilai=jenis_nilai,
                    nilai=Decimal(nilai_val)
                )
                messages.success(request, f"Nilai berhasil ditambahkan untuk {siswa.nama_lengkap}.")
                return redirect('guru_panel:nilai')
            except Exception as e:
                messages.error(request, f"Terjadi kesalahan: {str(e)}")
                
    siswa_list = Siswa.objects.all().order_by('nama_lengkap')
    kelas_list = Kelas.objects.all().order_by('nama_kelas')
    jenis_nilai_choices = Nilai.JENIS_NILAI_CHOICES
    
    context = {
        'siswa_list': siswa_list,
        'kelas_list': kelas_list,
        'mapel_diampu': mapel_diampu,
        'jenis_nilai_choices': jenis_nilai_choices,
        'is_single_mapel': mapel_diampu.count() == 1,
        'single_mapel': mapel_diampu.first() if mapel_diampu.count() == 1 else None
    }
    return render(request, 'guru_panel/input_nilai.html', context)
