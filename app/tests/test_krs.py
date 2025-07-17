import pytest
from rest_framework.test import APIClient
from app.models import MahasiswaDinus, TahunAjaran, SesiKuliah, Hari, MatkulKurikulum, JadwalTawar, KrsRecord

@pytest.mark.django_db
def test_krs():
    client = APIClient()

    # ──────────────── 1. Setup Data Dasar (Tahun Ajaran, Sesi, Hari) ────────────────
    ta = TahunAjaran.objects.create(
        kode="20241", tahun_awal="2024", tahun_akhir="2025",
        jns_smt=1, set_aktif=True
    )
    sesi1 = SesiKuliah.objects.create(jam="08:00-09:40", sks=2, jam_mulai="08:00", jam_selesai="09:40", status=1)
    sesi2 = SesiKuliah.objects.create(jam="10:00-11:40", sks=2, jam_mulai="10:00", jam_selesai="11:40", status=1)
    hari = Hari.objects.create(nama="Senin", nama_en="Monday")

    # ──────────────── 2. Setup Mahasiswa ────────────────
    mhs = MahasiswaDinus.objects.create(
        nim_dinus="4611414011", ta_masuk=2021,
        prodi="IF", kelas=1, akdm_stat="A"
    )

    # ──────────────── 3. Buat Matkul Sudah Diambil (IF101) ────────────────
    matkul1 = MatkulKurikulum.objects.create(
        kdmk="IF101", nmmk="Struktur Data", tp="T", sks=3, sks_t=2, sks_p=1,
        smt=3, jns_smt=1, aktif=True, kur_nama="Kurikulum 2020",
        kelompok_makul="MKK", kur_aktif=True, jenis_matkul="wajib"
    )
    jadwal1 = JadwalTawar.objects.create(
        ta=ta, kdmk=matkul1, klpk="A", kdds=1, jmax=30, jsisa=30,
        id_hari1=hari, id_sesi1=sesi1,
        id_sesi2=None, id_sesi3=None,
        id_ruang1=1, id_ruang2=1, id_ruang3=1,
        jns_jam=1, open_class=True
    )
    KrsRecord.objects.create(
        ta=ta, kdmk=matkul1, id_jadwal=jadwal1,
        nim_dinus=mhs, sts="A", sks=3
    )

    # ──────────────── 4. Buat Matkul Baru (IF102 dan IF103) ────────────────
    matkul2 = MatkulKurikulum.objects.create(
        kdmk="IF102", nmmk="Basis Data", tp="T", sks=3, sks_t=2, sks_p=1,
        smt=3, jns_smt=1, aktif=True, kur_nama="Kurikulum 2020",
        kelompok_makul="MKK", kur_aktif=True, jenis_matkul="wajib"
    )
    matkul3 = MatkulKurikulum.objects.create(
        kdmk="IF103", nmmk="Pemrograman Lanjut", tp="T", sks=3, sks_t=2, sks_p=1,
        smt=3, jns_smt=1, aktif=True, kur_nama="Kurikulum 2020",
        kelompok_makul="MKK", kur_aktif=True, jenis_matkul="wajib"
    )

    # ──────────────── 5. Jadwal untuk IF101 (baru), IF102, IF103 ────────────────
    jadwal1 = JadwalTawar.objects.create(
        ta=ta, kdmk=matkul1, klpk="B", kdds=2, jmax=30, jsisa=30,
        id_hari1=hari, id_sesi1=sesi2,
        id_sesi2=None, id_sesi3=None,
        id_ruang1=2, id_ruang2=2, id_ruang3=2,
        jns_jam=1, open_class=True
    )
    jadwal2 = JadwalTawar.objects.create(
        ta=ta, kdmk=matkul2, klpk="B", kdds=2, jmax=30, jsisa=30,
        id_hari1=hari, id_sesi1=sesi2,
        id_sesi2=None, id_sesi3=None,
        id_ruang1=2, id_ruang2=2, id_ruang3=2,
        jns_jam=1, open_class=True
    )
    jadwal3 = JadwalTawar.objects.create(
        ta=ta, kdmk=matkul3, klpk="B", kdds=2, jmax=30, jsisa=30,
        id_hari1=hari, id_sesi1=sesi2,
        id_sesi2=None, id_sesi3=None,
        id_ruang1=2, id_ruang2=2, id_ruang3=2,
        jns_jam=1, open_class=True
    )

    # ──────────────── 6. Tes GET /students/{nim}/krs/current/ ────────────────
    url_krs = f"/api/v1/students/{mhs.nim_dinus}/krs/current/"
    response_krs = client.get(url_krs)
    assert response_krs.status_code == 200
    assert isinstance(response_krs.data, list)
    assert any(item.get("kdmk", {}).get("kdmk") == "IF101" for item in response_krs.data)

    # ──────────────── 7. Tes GET /courses/available/ ────────────────
    url_avail = f"/api/v1/students/{mhs.nim_dinus}/courses/available/"
    response_avail = client.get(url_avail)
    print("DEBUG AVAILABLE COURSES:", response_avail.data)
    assert response_avail.status_code == 200
    assert isinstance(response_avail.data, list)
    assert any(item["kdmk"]["kdmk"] == "IF101" for item in response_krs.data)

    # ──────────────── 8. Tambah Matkul ke KRS via POST /krs/courses/ ────────────────
    url_post = f"/api/v1/students/{mhs.nim_dinus}/krs/courses/"
    response_post_1 = client.post(url_post, {"id_jadwal": jadwal1.id}, format="json")
    assert response_post_1.status_code == 201
    response_post_2 = client.post(url_post, {"id_jadwal": jadwal2.id}, format="json")
    assert response_post_2.status_code == 201
    response_post = client.post(url_post, {"id_jadwal": jadwal3.id}, format="json")
    assert response_post.status_code == 201
    assert "message" in response_post.data
    assert response_post.data["message"] == "Mata kuliah berhasil ditambahkan ke KRS."
    assert response_post.data["data"]["kdmk"]["kdmk"] == "IF103"

    # ──────────────── 9. Hapus matkul dari KRS ────────────────
    url_delete = f"/api/v1/students/{mhs.nim_dinus}/krs/courses/{jadwal3.id}/"
    response_delete = client.delete(url_delete)
    assert response_delete.status_code == 200
    assert response_delete.data["message"] == "Mata kuliah berhasil dihapus dari KRS."

    # ──────────────── 10. Pastikan IF103 sudah tidak ada ────────────────
    response_krs = client.get(url_krs)
    assert all(item["kdmk"]["kdmk"] != "IF103" for item in response_krs.data)

    # ──────────────── 11. Tes GET /students/{nim}/krs/status/ ────────────────
    url_status = f"/api/v1/students/{mhs.nim_dinus}/krs/status/"
    response_status = client.get(url_status)

    assert response_status.status_code == 200
    assert "validated" in response_status.data
    assert "total_sks" in response_status.data
    assert "ips_last_semester" in response_status.data
    assert response_status.data["validated"] is False
    assert response_status.data["total_sks"] == 9
    assert response_status.data["ips_last_semester"] is None
