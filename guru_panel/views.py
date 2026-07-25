from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from accounts.models import Siswa
from akademik.models import Kelas, Nilai, Raport, MataPelajaran, Jadwal, TahunAjaran

def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profil_guru') and request.user.profil_guru.posisi == 'Kepala Sekolah':
            return redirect('kepsek_panel:dashboard')
        return redirect('guru_panel:dashboard')
        
    if request.method == 'POST':
        nip = request.POST.get('nip')
        password = request.POST.get('password')
        user = authenticate(request, username=nip, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'profil_guru') and user.profil_guru.posisi == 'Kepala Sekolah':
                return redirect('kepsek_panel:dashboard')
            return redirect('guru_panel:dashboard')
        else:
            messages.error(request, 'NIP atau Password salah.')
            
    return render(request, 'guru_panel/login.html')

def logout_view(request):
    logout(request)
    return redirect('guru_panel:login')

from django.core.paginator import Paginator

@login_required(login_url='guru_panel:login')
def dashboard_view(request):
    return render(request, 'guru_panel/dashboard.html')

@login_required(login_url='guru_panel:login')
def siswa_view(request):
    siswa_list = Siswa.objects.all().order_by('nama_lengkap')
    paginator = Paginator(siswa_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'guru_panel/siswa.html', {'page_obj': page_obj})

@login_required(login_url='guru_panel:login')
def kelas_view(request):
    kelas_list = Kelas.objects.all().select_related('wali_kelas', 'tahun_ajaran').order_by('nama_kelas')
    return render(request, 'guru_panel/kelas.html', {'kelas_list': kelas_list})

@login_required(login_url='guru_panel:login')
def nilai_view(request):
    nilai_list = Nilai.objects.all().select_related('siswa', 'kelas', 'mata_pelajaran').order_by('-tanggal')
    paginator = Paginator(nilai_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'guru_panel/nilai.html', {'page_obj': page_obj})

@login_required(login_url='guru_panel:login')
def raport_view(request):
    raport_list = Raport.objects.all().select_related('siswa', 'kelas').order_by('siswa__nama_lengkap')
    paginator = Paginator(raport_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'guru_panel/raport.html', {'page_obj': page_obj})

@login_required(login_url='guru_panel:login')
def jadwal_view(request):
    tahun_ajaran_aktif = TahunAjaran.objects.filter(is_active=True).first()
    kelas_list = Kelas.objects.all().order_by('nama_kelas')
    
    selected_kelas_id = request.GET.get('kelas_id')
    selected_kelas = None
    
    if selected_kelas_id:
        selected_kelas = Kelas.objects.filter(id=selected_kelas_id).first()
        
    if not selected_kelas:
        if hasattr(request.user, 'profil_guru'):
            selected_kelas = Kelas.objects.filter(wali_kelas=request.user.profil_guru).first()
        if not selected_kelas:
            selected_kelas = kelas_list.first()

    jadwal_list = []
    if selected_kelas:
        jadwal_list = list(Jadwal.objects.filter(kelas=selected_kelas).select_related('mata_pelajaran', 'mata_pelajaran__guru_pengampu'))
        # Urutkan berdasarkan hari kerja
        hari_order = {'Senin': 0, 'Selasa': 1, 'Rabu': 2, 'Kamis': 3, 'Jumat': 4, 'Sabtu': 5}
        jadwal_list.sort(key=lambda x: (hari_order.get(x.hari, 99), x.jam))
        
    context = {
        'tahun_ajaran_aktif': tahun_ajaran_aktif,
        'kelas_list': kelas_list,
        'selected_kelas': selected_kelas,
        'jadwal_list': jadwal_list,
    }
    return render(request, 'guru_panel/jadwal.html', context)

@login_required(login_url='guru_panel:login')
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
