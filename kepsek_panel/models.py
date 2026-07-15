from django.db import models
from guru_panel.models import CutiGuru, PengajuanAnggaran
from akademik.models import Raport, PendaftarPPDB, MutasiSiswa

class PersetujuanCuti(CutiGuru):
    class Meta:
        proxy = True
        verbose_name = "Persetujuan Cuti"
        verbose_name_plural = "Persetujuan Cuti"

class PersetujuanAnggaran(PengajuanAnggaran):
    class Meta:
        proxy = True
        verbose_name = "Persetujuan Anggaran"
        verbose_name_plural = "Persetujuan Anggaran"

class TandaTanganRaport(Raport):
    class Meta:
        proxy = True
        verbose_name = "Tanda Tangan Raport"
        verbose_name_plural = "Tanda Tangan Raport"

class LaporanPPDB(PendaftarPPDB):
    class Meta:
        proxy = True
        verbose_name = "Laporan PPDB"
        verbose_name_plural = "Laporan PPDB"

class LaporanMutasi(MutasiSiswa):
    class Meta:
        proxy = True
        verbose_name = "Laporan Mutasi"
        verbose_name_plural = "Laporan Mutasi"

class LaporanKelulusan(Raport):
    class Meta:
        proxy = True
        verbose_name = "Laporan Kelulusan"
        verbose_name_plural = "Laporan Kelulusan"
