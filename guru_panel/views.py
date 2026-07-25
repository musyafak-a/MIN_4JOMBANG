from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Siswa
from akademik.models import Kelas, Nilai, Raport, MataPelajaran

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

@login_required(login_url='guru_panel:login')
def dashboard_view(request):
    return render(request, 'guru_panel/dashboard.html')

@login_required(login_url='guru_panel:login')
def siswa_view(request):
    siswa_list = Siswa.objects.all().order_by('nama_lengkap')
    return render(request, 'guru_panel/siswa.html', {'siswa_list': siswa_list})

@login_required(login_url='guru_panel:login')
def kelas_view(request):
    kelas_list = Kelas.objects.all().order_by('nama_kelas')
    return render(request, 'guru_panel/kelas.html', {'kelas_list': kelas_list})

@login_required(login_url='guru_panel:login')
def nilai_view(request):
    nilai_list = Nilai.objects.all().order_by('-tanggal')
    return render(request, 'guru_panel/nilai.html', {'nilai_list': nilai_list})

@login_required(login_url='guru_panel:login')
def raport_view(request):
    raport_list = Raport.objects.all().order_by('siswa__nama_lengkap')
    return render(request, 'guru_panel/raport.html', {'raport_list': raport_list})

@login_required(login_url='guru_panel:login')
def jadwal_view(request):
    mapel_list = MataPelajaran.objects.all().order_by('nama_mapel')
    return render(request, 'guru_panel/jadwal.html', {'mapel_list': mapel_list})
