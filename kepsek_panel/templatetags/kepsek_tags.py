from django import template
from guru_panel.models import CutiGuru, PengajuanAnggaran
from akademik.models import Raport, Siswa

register = template.Library()

@register.simple_tag
def get_total_siswa():
    return Siswa.objects.count()

@register.simple_tag
def get_total_cuti():
    return CutiGuru.objects.filter(status='Menunggu').count()

@register.simple_tag
def get_total_anggaran():
    return PengajuanAnggaran.objects.filter(status='Menunggu').count()

@register.simple_tag
def get_total_raport():
    return Raport.objects.filter(is_signed_by_kepsek=False).count()
