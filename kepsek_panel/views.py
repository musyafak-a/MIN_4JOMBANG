from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from guru_panel.models import CutiGuru, PengajuanAnggaran
from akademik.models import Raport, PendaftarPPDB, MutasiSiswa, Siswa

def is_kepsek(user):
    return user.is_authenticated and hasattr(user, 'profil_guru') and user.profil_guru.posisi == 'Kepala Sekolah'

@login_required
@user_passes_test(is_kepsek)
def dashboard(request):
    total_cuti_menunggu = CutiGuru.objects.filter(status='Menunggu').count()
    total_anggaran_menunggu = PengajuanAnggaran.objects.filter(status='Menunggu').count()
    total_raport_belum_ttd = Raport.objects.filter(is_signed_by_kepsek=False).count()
    total_siswa = Siswa.objects.count()
    
    context = {
        'total_cuti_menunggu': total_cuti_menunggu,
        'total_anggaran_menunggu': total_anggaran_menunggu,
        'total_raport_belum_ttd': total_raport_belum_ttd,
        'total_siswa': total_siswa,
    }
    return render(request, 'kepsek_panel/dashboard.html', context)

@login_required
@user_passes_test(is_kepsek)
def persetujuan_cuti(request):
    cuti_list = CutiGuru.objects.all().order_by('-tanggal_pengajuan')
    return render(request, 'kepsek_panel/persetujuan_cuti.html', {'cuti_list': cuti_list})

@login_required
@user_passes_test(is_kepsek)
def action_cuti(request, cuti_id, action):
    cuti = get_object_or_404(CutiGuru, id=cuti_id)
    if action == 'approve':
        cuti.status = 'Disetujui'
        messages.success(request, f"Cuti {cuti.guru.nama_lengkap} disetujui.")
    elif action == 'reject':
        cuti.status = 'Ditolak'
        messages.warning(request, f"Cuti {cuti.guru.nama_lengkap} ditolak.")
    cuti.save()
    return redirect('kepsek_panel:persetujuan_cuti')

@login_required
@user_passes_test(is_kepsek)
def persetujuan_anggaran(request):
    anggaran_list = PengajuanAnggaran.objects.all().order_by('-tanggal_pengajuan')
    return render(request, 'kepsek_panel/persetujuan_anggaran.html', {'anggaran_list': anggaran_list})

@login_required
@user_passes_test(is_kepsek)
def action_anggaran(request, anggaran_id, action):
    anggaran = get_object_or_404(PengajuanAnggaran, id=anggaran_id)
    if action == 'approve':
        anggaran.status = 'Disetujui'
        messages.success(request, f"Anggaran {anggaran.judul} disetujui.")
    elif action == 'reject':
        anggaran.status = 'Ditolak'
        messages.warning(request, f"Anggaran {anggaran.judul} ditolak.")
    anggaran.save()
    return redirect('kepsek_panel:persetujuan_anggaran')

@login_required
@user_passes_test(is_kepsek)
def tanda_tangan_raport(request):
    raport_list = Raport.objects.all().select_related('siswa', 'kelas').order_by('kelas__nama_kelas', 'siswa__nama_lengkap')
    return render(request, 'kepsek_panel/tanda_tangan_raport.html', {'raport_list': raport_list})

@login_required
@user_passes_test(is_kepsek)
def sign_raport(request, raport_id):
    raport = get_object_or_404(Raport, id=raport_id)
    if not raport.is_signed_by_kepsek:
        raport.is_signed_by_kepsek = True
        raport.signature_date = timezone.now().date()
        raport.save()
        messages.success(request, f"Raport {raport.siswa.nama_lengkap} berhasil ditandatangani.")
    return redirect('kepsek_panel:tanda_tangan_raport')

@login_required
@user_passes_test(is_kepsek)
def laporan_ppdb(request):
    pendaftar_list = PendaftarPPDB.objects.all().order_by('-tanggal_daftar')
    return render(request, 'kepsek_panel/laporan_ppdb.html', {'pendaftar_list': pendaftar_list})

@login_required
@user_passes_test(is_kepsek)
def laporan_mutasi(request):
    mutasi_list = MutasiSiswa.objects.all().order_by('-tanggal')
    return render(request, 'kepsek_panel/laporan_mutasi.html', {'mutasi_list': mutasi_list})

@login_required
@user_passes_test(is_kepsek)
def laporan_kelulusan(request):
    # Asumsi lulus jika kelas tingkat 6 dan status_naik_kelas (dalam hal ini artinya lulus)
    kelulusan_list = Raport.objects.filter(kelas__tingkat='6', status_naik_kelas=True).select_related('siswa', 'kelas')
    return render(request, 'kepsek_panel/laporan_kelulusan.html', {'kelulusan_list': kelulusan_list})

