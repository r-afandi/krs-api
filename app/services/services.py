from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import MahasiswaDinus, MatkulKurikulum, Hari, JadwalTawar, SesiKuliah, TahunAjaran, KrsRecord,DaftarNilai
from app.serializers import (MahasiswaDinusSerializer, MatkulKurikulumSerializer,
                            HariSerializer, JadwalTawarSerializer, SesiKuliahSerializer,
                            TahunAjaranSerializer, KrsRecordSerializer)
from django.db.models import Q
def get_krs_mahasiswa(nim):
    print("DEBUG: get_krs_mahasiswa() called with nim =", nim)
    try:
        mahasiswa = MahasiswaDinus.objects.get(nim_dinus=nim)
        print("DEBUG: Mahasiswa found:", mahasiswa.nim_dinus)

        krs_records = KrsRecord.objects.filter(nim_dinus=mahasiswa)
        print("DEBUG: KRS count:", krs_records.count())

        if not krs_records:
            raise ValueError("KRS not found for the given student.")

        serializer = KrsRecordSerializer(krs_records, many=True)
        return serializer.data

    except MahasiswaDinus.DoesNotExist:
        raise ValueError("Mahasiswa with the given NIM does not exist.")

    except KrsRecord.DoesNotExist:
        raise ValueError("KRS for the given student does not exist.")
def get_available_courses(nim):
    mahasiswa = MahasiswaDinus.objects.get(nim_dinus=nim)
    krs_aktif = KrsRecord.objects.filter(nim_dinus=mahasiswa)
    nilai_A = KrsRecord.objects.filter(nim_dinus=mahasiswa, daftar_nilai__nilai='A').values_list('kdmk', flat=True)
    
    jadwal_bentrok = get_conflicting_jadwals(krs_aktif)  # kamu perlu buat logic cek bentrok
    
    available_courses = JadwalTawar.objects.exclude(
        id__in=jadwal_bentrok
    ).exclude(
        kdmk__in=nilai_A
    )
    
    return available_courses


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
    konflik_filter = Q()
    for hari, sesi in konflik:
        konflik_filter |= (
            Q(id_hari1=hari, id_sesi1=sesi) |
            Q(id_hari2=hari, id_sesi2=sesi) |
            Q(id_hari3=hari, id_sesi3=sesi)
        )

    return JadwalTawar.objects.filter(konflik_filter).values_list('id', flat=True)

def get_available_courses_for_student(nim):
    try:
        mahasiswa = MahasiswaDinus.objects.get(nim_dinus=nim)
    except MahasiswaDinus.DoesNotExist:
        return None, "Mahasiswa tidak ditemukan."

    krs_aktif = KrsRecord.objects.filter(nim_dinus=mahasiswa)
    if not krs_aktif.exists():
        return [], "Mahasiswa belum memiliki KRS aktif."

    nilai_A = DaftarNilai.objects.filter(
        nim_dinus=mahasiswa, nl='A'
    ).values_list('kdmk__kdmk', flat=True)

    jadwal_bentrok_ids = get_conflicting_jadwals(krs_aktif)

    kur_nama = (
        DaftarNilai.objects
        .filter(nim_dinus=mahasiswa)
        .select_related('kdmk')
        .values_list('kdmk__kur_nama', flat=True)
        .distinct()
        .first()
    )

    available = JadwalTawar.objects.exclude(
        id__in=jadwal_bentrok_ids
    ).exclude(
        kdmk__kdmk__in=nilai_A
    )

    if kur_nama:
        available = available.filter(kdmk__kur_nama=kur_nama)

    serialized = JadwalTawarSerializer(available, many=True)
    return serialized.data, None
