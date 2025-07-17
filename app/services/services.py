
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import MahasiswaDinus, MatkulKurikulum, Hari, JadwalTawar, SesiKuliah, TahunAjaran, KrsRecord,DaftarNilai,ValidasiKrsMhs, IPSemester
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
# Mengambil seluruh KRS milik mahasiswa berdasarkan NIM
def get_krs_mahasiswa(nim):
    try:
        mahasiswa = MahasiswaDinus.objects.get(nim_dinus=nim)
        krs_records = KrsRecord.objects.filter(nim_dinus=mahasiswa)

        if not krs_records.exists():
            return None, "KRS tidak ditemukan untuk mahasiswa ini."

        return krs_records, None

    except MahasiswaDinus.DoesNotExist:
        return None, "Mahasiswa tidak ditemukan."

    except Exception as e:
        return None, str(e)

# Mendapatkan semua jadwal yang bentrok dari daftar KRS aktif mahasiswa
def get_conflicting_jadwals(krs_aktif):
    jadwal_ids = krs_aktif.values_list('id_jadwal', flat=True)
    existing_jadwal = JadwalTawar.objects.filter(id__in=jadwal_ids)

    konflik = []
    for jadwal in existing_jadwal:
        for hari, sesi in [
            (jadwal.id_hari1_id, jadwal.id_sesi1_id),
            (jadwal.id_hari2_id, jadwal.id_sesi2_id),
            (jadwal.id_hari3_id, jadwal.id_sesi3_id),
        ]:
            if hari and sesi:
                konflik.append((hari, sesi))

    # Buat filter OR untuk mendeteksi jadwal bentrok
    konflik_filter = Q()
    for hari, sesi in konflik:
        konflik_filter |= (
            Q(id_hari1=hari, id_sesi1=sesi) |
            Q(id_hari2=hari, id_sesi2=sesi) |
            Q(id_hari3=hari, id_sesi3=sesi)
        )

    return JadwalTawar.objects.filter(konflik_filter).select_related("kdmk")

# Mendapatkan list mata kuliah yang bisa diambil oleh mahasiswa (tanpa jadwal)
def get_available_courses(nim):
    try:
        mahasiswa = MahasiswaDinus.objects.get(nim_dinus=nim)
        krs_aktif = KrsRecord.objects.filter(nim_dinus=mahasiswa)

        # Ambil matkul yang sudah dapat nilai A
        nilai_A = KrsRecord.objects.filter(
            nim_dinus=mahasiswa, daftar_nilai__nilai='A'
        ).values_list('kdmk__kdmk', flat=True)

        # Deteksi jadwal bentrok
        jadwal_bentrok = get_conflicting_jadwals(krs_aktif)
        kdmk_bentrok = jadwal_bentrok.values_list("kdmk__kdmk", flat=True)

        # Filter matkul yang masih bisa diambil
        available_courses = MatkulKurikulum.objects.filter(
            aktif=True, kur_aktif=True
        ).exclude(
            kdmk__in=nilai_A
        ).exclude(
            kdmk__in=kdmk_bentrok
        )

        return available_courses, None

    except MahasiswaDinus.DoesNotExist:
        return None, "Mahasiswa tidak ditemukan."
    except Exception as e:
        return None, str(e)

# Mendapatkan jadwal kuliah yang masih bisa diambil oleh mahasiswa
def get_available_courses_for_student(nim):
    try:
        mahasiswa = MahasiswaDinus.objects.get(nim_dinus=nim)
    except MahasiswaDinus.DoesNotExist:
        return None, "Mahasiswa tidak ditemukan."

    # Ambil KRS aktif
    krs_aktif = KrsRecord.objects.filter(nim_dinus=mahasiswa)
    if not krs_aktif.exists():
        return [], "Mahasiswa belum memiliki KRS aktif."

    # Cek matkul yang sudah dapat A
    nilai_A = DaftarNilai.objects.filter(
        nim_dinus=mahasiswa, nl='A'
    ).values_list('kdmk__kdmk', flat=True)

    # Deteksi jadwal bentrok
    jadwal_bentrok_ids = get_conflicting_jadwals(krs_aktif)

    # Deteksi kurikulum mahasiswa
    kur_nama = (
        DaftarNilai.objects
        .filter(nim_dinus=mahasiswa)
        .select_related('kdmk')
        .values_list('kdmk__kur_nama', flat=True)
        .distinct()
        .first()
    )

    # Filter jadwal yang bisa diambil
    available = JadwalTawar.objects.exclude(
        id__in=jadwal_bentrok_ids
    ).exclude(
        kdmk__kdmk__in=nilai_A
    )

    # Batasi hanya kurikulum milik mahasiswa
    if kur_nama:
        available = available.filter(kdmk__kur_nama=kur_nama)

    return available, None 

# Menambahkan mata kuliah ke dalam KRS mahasiswa
def add_course_to_krs(nim, id_jadwal):
    try:
        mahasiswa = MahasiswaDinus.objects.get(nim_dinus=nim)
    except MahasiswaDinus.DoesNotExist:
        return None, "Mahasiswa tidak ditemukan."

    try:
        jadwal = JadwalTawar.objects.select_related("kdmk").get(id=id_jadwal)
    except JadwalTawar.DoesNotExist:
        return None, "Jadwal tidak ditemukan."

    matkul = jadwal.kdmk
    nama_mk = matkul.nmmk

    # Cek kuota
    if jadwal.jsisa <= 0:
        return None, f"Kelas '{nama_mk}' sudah penuh."

    # Cek kurikulum aktif
    if not matkul.kur_nama or not matkul.kur_aktif:
        return None, f"Mata kuliah '{nama_mk}' tidak termasuk dalam kurikulum aktif."

    # Cek kesesuaian kurikulum
    daftar_nilai = DaftarNilai.objects.filter(nim_dinus=mahasiswa)
    kur_mahasiswa = daftar_nilai.values_list("kdmk__kur_nama", flat=True).first()
    if kur_mahasiswa and matkul.kur_nama != kur_mahasiswa:
        return None, f"Mata kuliah '{nama_mk}' tidak sesuai dengan kurikulum mahasiswa."

    # Cek apakah sudah pernah lulus
    if daftar_nilai.filter(kdmk=matkul).exists():
        return None, f"Kamu sudah lulus '{nama_mk}'."

    # Cek bentrok jadwal
    krs_terdaftar = KrsRecord.objects.select_related("id_jadwal").filter(
        nim_dinus=mahasiswa,
        kdmk=matkul
    )

    for krs in krs_terdaftar:
        existing = krs.id_jadwal
        if existing.id_hari1 == jadwal.id_hari1 and existing.id_sesi1 == jadwal.id_sesi1:
            return None, (
                f"Jadwal '{nama_mk}' bentrok dengan '{existing.kdmk.nmmk}' pada hari "
                f"{existing.id_hari1.nama}, sesi {existing.id_sesi1.id}."
            )

    # Tambahkan ke KRS
    with transaction.atomic():
        new_krs = KrsRecord.objects.create(
            ta=jadwal.ta,
            kdmk=matkul,
            id_jadwal=jadwal,
            nim_dinus=mahasiswa,
            sts='A',
            sks=matkul.sks,
            modul=0,
        )
        jadwal.jsisa -= 1
        jadwal.save()

    return new_krs, None

# Menghapus mata kuliah dari KRS mahasiswa
def remove_krs_course(nim: str, id_jadwal: str) -> dict:
    mahasiswa_dinus = get_object_or_404(MahasiswaDinus, nim_dinus=nim)

    try:
        krs_record = KrsRecord.objects.get(
            nim_dinus=mahasiswa_dinus,
            id_jadwal=id_jadwal,
        )
    except KrsRecord.DoesNotExist:
        raise ValidationError("Mata kuliah tidak ditemukan atau KRS sudah tervalidasi.")

    # Hapus KRS
    with transaction.atomic():
        krs_record.delete()

    return {
        "message": "Mata kuliah berhasil dihapus dari KRS.",
        "nim": nim,
        "id_jadwal": id_jadwal
    }

# Mengambil status validasi KRS mahasiswa (tervalidasi, total sks, ip terakhir)
def get_krs_status(nim_dinus):
    current_ta = TahunAjaran.objects.filter(set_aktif=True).first()
    if not current_ta:
        raise Exception("Tahun Ajaran aktif tidak ditemukan.")

    # Cek validasi
    validasi = ValidasiKrsMhs.objects.filter(nim_dinus=nim_dinus, ta=current_ta.kode).first()
    is_validated = bool(validasi)

    # Hitung SKS
    total_sks = KrsRecord.objects.filter(
        nim_dinus__nim_dinus=nim_dinus,
        ta=current_ta
    ).aggregate(sks_total=Sum('sks'))['sks_total'] or 0

    # Ambil IPS terakhir
    ip_data = IPSemester.objects.filter(nim_dinus=nim_dinus).order_by('-ta').first()
    ips = ip_data.ips if ip_data else None

    return {
        'validated': is_validated,
        'total_sks': total_sks,
        'ips_last_semester': ips
    }
