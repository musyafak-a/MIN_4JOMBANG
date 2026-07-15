from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.models import Berita, Pengumuman
from django.utils.text import slugify

def is_admin_sekolah(user):
    return user.is_authenticated and hasattr(user, 'profil_admin_sekolah')

@login_required
@user_passes_test(is_admin_sekolah)
def dashboard(request):
    total_berita = Berita.objects.count()
    total_pengumuman = Pengumuman.objects.count()
    
    context = {
        'total_berita': total_berita,
        'total_pengumuman': total_pengumuman,
    }
    return render(request, 'admin_sekolah_panel/dashboard.html', context)

# --- Kelola Berita ---

@login_required
@user_passes_test(is_admin_sekolah)
def kelola_berita(request):
    berita_list = Berita.objects.all().order_by('-tanggal_publikasi')
    return render(request, 'admin_sekolah_panel/kelola_berita.html', {'berita_list': berita_list})

@login_required
@user_passes_test(is_admin_sekolah)
def form_berita(request, id=None):
    berita = get_object_or_404(Berita, id=id) if id else None
    if request.method == 'POST':
        judul = request.POST.get('judul')
        konten = request.POST.get('konten')
        status = request.POST.get('status')
        gambar = request.FILES.get('gambar')
        
        if not berita:
            berita = Berita(penulis=request.user)
            berita.slug = slugify(judul)
            
        berita.judul = judul
        berita.konten = konten
        berita.status = status
        if gambar:
            berita.gambar = gambar
        berita.save()
        messages.success(request, 'Berita berhasil disimpan!')
        return redirect('admin_sekolah_panel:kelola_berita')
        
    return render(request, 'admin_sekolah_panel/form_berita.html', {'berita': berita})

@login_required
@user_passes_test(is_admin_sekolah)
def hapus_berita(request, id):
    berita = get_object_or_404(Berita, id=id)
    berita.delete()
    messages.success(request, 'Berita berhasil dihapus!')
    return redirect('admin_sekolah_panel:kelola_berita')

# --- Kelola Pengumuman ---

@login_required
@user_passes_test(is_admin_sekolah)
def kelola_pengumuman(request):
    pengumuman_list = Pengumuman.objects.all().order_by('-tanggal_publikasi')
    return render(request, 'admin_sekolah_panel/kelola_pengumuman.html', {'pengumuman_list': pengumuman_list})

@login_required
@user_passes_test(is_admin_sekolah)
def form_pengumuman(request, id=None):
    pengumuman = get_object_or_404(Pengumuman, id=id) if id else None
    if request.method == 'POST':
        judul = request.POST.get('judul')
        isi = request.POST.get('isi')
        status = request.POST.get('status')
        gambar = request.FILES.get('gambar')
        
        if not pengumuman:
            pengumuman = Pengumuman(penulis=request.user)
            pengumuman.slug = slugify(judul)
            
        pengumuman.judul = judul
        pengumuman.isi = isi
        pengumuman.status = status
        if gambar:
            pengumuman.gambar = gambar
        pengumuman.save()
        messages.success(request, 'Pengumuman berhasil disimpan!')
        return redirect('admin_sekolah_panel:kelola_pengumuman')
        
    return render(request, 'admin_sekolah_panel/form_pengumuman.html', {'pengumuman': pengumuman})

@login_required
@user_passes_test(is_admin_sekolah)
def hapus_pengumuman(request, id):
    pengumuman = get_object_or_404(Pengumuman, id=id)
    pengumuman.delete()
    messages.success(request, 'Pengumuman berhasil dihapus!')
    return redirect('admin_sekolah_panel:kelola_pengumuman')
