import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time

# Sesuaikan import model dengan lokasi model Anda
# Contoh: from your_app.models import MyModel, AnotherModel
# Ganti 'your_app' dengan nama aplikasi Django Anda yang sebenarnya
from app.models import (
    TahunAjaran, MahasiswaDinus, MatkulKurikulum, Hari, Ruang,
    SesiKuliah, SesiKuliahBentrok, JadwalTawar, KrsRecord, DaftarNilai,
    ValidasiKrsMhs, IPSemester
)

import os

class Command(BaseCommand):
    help = 'Loads dummy data from a JSON string into the database.'

    def handle(self, *args, **options):
        self.stdout.write("Memulai pembuatan data dummy dari dummy.json...")

        # Mendapatkan path direktori dari file management command saat ini.
        # Ini akan menjadi 'your_project/your_app/management/commands/'
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Asumsi 1: dummy.json berada di folder yang SAMA dengan file load_dummy_data.py
        json_file_path = os.path.join(base_dir, 'dummy.json')

        # Asumsi 2: dummy.json berada di ROOT direktori proyek Django Anda
        # (tempat manage.py berada)
        # from django.conf import settings
        # json_file_path = os.path.join(settings.BASE_DIR, 'dummy.json')

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                dummy_data = json.load(f)
            self.stdout.write(self.style.SUCCESS(f"Berhasil memuat data dari {json_file_path}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: File dummy.json tidak ditemukan di {json_file_path}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error parsing dummy.json: {e}"))
            return
        # Fungsi pembantu untuk parsing tanggal/waktu
        def parse_datetime(dt_str):
            if dt_str:
                return timezone.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return None

        def parse_date(d_str):
            if d_str:
                return date.fromisoformat(d_str)
            return None

        def parse_time(t_str):
            if t_str:
                return time.fromisoformat(t_str)
            return None

        self.stdout.write("Creating TahunAjaran data...")
        for data in dummy_data["TahunAjaran"]:
            TahunAjaran.objects.get_or_create(
                kode=data['kode'],
                defaults={
                    'tahun_akhir': data['tahun_akhir'],
                    'tahun_awal': data['tahun_awal'],
                    'jns_smt': data['jns_smt'],
                    'set_aktif': data['set_aktif'],
                    'buku_tagih_jenis': data['buku_tagih_jenis'],
                    'update_time': parse_datetime(data['update_time']),
                    'update_id': data['update_id'],
                    'update_host': data['update_host'],
                    'added_time': parse_datetime(data['added_time']),
                    'added_id': data['added_id'],
                    'added_host': data['added_host'],
                    'tgl_masuk': parse_date(data['tgl_masuk'])
                }
            )
        self.stdout.write(self.style.SUCCESS('TahunAjaran data created/updated successfully.'))

        self.stdout.write("Creating MahasiswaDinus data...")
        for data in dummy_data["MahasiswaDinus"]:
            MahasiswaDinus.objects.get_or_create(
                nim_dinus=data['nim_dinus'],
                defaults={
                    'ta_masuk': data['ta_masuk'],
                    'prodi': data['prodi'],
                    'pass_mhs': data['pass_mhs'],
                    'kelas': data['kelas'],
                    'akdm_stat': data['akdm_stat']
                }
            )
        self.stdout.write(self.style.SUCCESS('MahasiswaDinus data created/updated successfully.'))

        self.stdout.write("Creating MatkulKurikulum data...")
        for data in dummy_data["MatkulKurikulum"]:
            MatkulKurikulum.objects.get_or_create(
                kdmk=data['kdmk'],
                defaults={
                    'nmmk': data['nmmk'],
                    'nmen': data['nmen'],
                    'tp': data['tp'],
                    'sks': data['sks'],
                    'sks_t': data['sks_t'],
                    'sks_p': data['sks_p'],
                    'smt': data['smt'],
                    'jns_smt': data['jns_smt'],
                    'aktif': data['aktif'],
                    'kur_nama': data['kur_nama'],
                    'kelompok_makul': data['kelompok_makul'],
                    'kur_aktif': data['kur_aktif'],
                    'jenis_matkul': data['jenis_matkul']
                }
            )
        self.stdout.write(self.style.SUCCESS('MatkulKurikulum data created/updated successfully.'))

        self.stdout.write("Creating Hari data...")
        for data in dummy_data["Hari"]:
            Hari.objects.get_or_create(
                id=data['id'],
                defaults={
                    'nama': data['nama'],
                    'nama_en': data['nama_en']
                }
            )
        self.stdout.write(self.style.SUCCESS('Hari data created/updated successfully.'))

        self.stdout.write("Creating Ruang data...")
        for data in dummy_data["Ruang"]:
            Ruang.objects.get_or_create(
                nama=data['nama'],
                defaults={
                    'nama2': data['nama2'],
                    'id_jenis_makul': data['id_jenis_makul'],
                    'id_fakultas': data['id_fakultas'],
                    'kapasitas': data['kapasitas'],
                    'kap_ujian': data['kap_ujian'],
                    'status': data['status'],
                    'luas': data['luas'],
                    'kondisi': data['kondisi'],
                    'jumlah': data['jumlah']
                }
            )
        self.stdout.write(self.style.SUCCESS('Ruang data created/updated successfully.'))

        self.stdout.write("Creating SesiKuliah data...")
        for data in dummy_data["SesiKuliah"]:
            SesiKuliah.objects.get_or_create(
                id=data['id'],
                defaults={
                    'jam': data['jam'],
                    'sks': data['sks'],
                    'jam_mulai': parse_time(data['jam_mulai']),
                    'jam_selesai': parse_time(data['jam_selesai']),
                    'status': data['status']
                }
            )
        self.stdout.write(self.style.SUCCESS('SesiKuliah data created/updated successfully.'))

        self.stdout.write("Creating SesiKuliahBentrok data...")
        for data in dummy_data["SesiKuliahBentrok"]:
            try:
                sesi_bentrok_obj = SesiKuliah.objects.get(id=data['sesi_bentrok'])
                sesi_bentrok_dengan_obj = SesiKuliah.objects.get(id=data['sesi_bentrok_dengan'])
                SesiKuliahBentrok.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'sesi_bentrok': sesi_bentrok_obj,
                        'sesi_bentrok_dengan': sesi_bentrok_dengan_obj
                    }
                )
            except SesiKuliah.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f"Error creating SesiKuliahBentrok: {e} for IDs {data['sesi_bentrok']} or {data['sesi_bentrok_dengan']}"))
        self.stdout.write(self.style.SUCCESS('SesiKuliahBentrok data created/updated successfully.'))

        self.stdout.write("Creating JadwalTawar data...")
        for data in dummy_data["JadwalTawar"]:
            try:
                ta_obj = TahunAjaran.objects.get(kode=data['ta'])
                kdmk_obj = MatkulKurikulum.objects.get(kdmk=data['kdmk'])
                hari1_obj = Hari.objects.get(id=data['id_hari1']) if data['id_hari1'] else None
                sesi1_obj = SesiKuliah.objects.get(id=data['id_sesi1']) if data['id_sesi1'] else None

                JadwalTawar.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'ta': ta_obj,
                        'kdmk': kdmk_obj,
                        'klpk': data['klpk'],
                        'klpk_2': data['klpk_2'],
                        'kdds': data['kdds'],
                        'kdds2': data['kdds2'],
                        'jmax': data['jmax'],
                        'jsisa': data['jsisa'],
                        'id_hari1': hari1_obj,
                        'id_hari2': Hari.objects.get(id=data['id_hari2']) if data['id_hari2'] else None,
                        'id_hari3': Hari.objects.get(id=data['id_hari3']) if data['id_hari3'] else None,
                        'id_sesi1': sesi1_obj,
                        'id_sesi2': SesiKuliah.objects.get(id=data['id_sesi2']) if data['id_sesi2'] else None,
                        'id_sesi3': SesiKuliah.objects.get(id=data['id_sesi3']) if data['id_sesi3'] else None,
                        'id_ruang1': data['id_ruang1'],
                        'id_ruang2': data['id_ruang2'],
                        'id_ruang3': data['id_ruang3'],
                        'jns_jam': data['jns_jam'],
                        'open_class': data['open_class']
                    }
                )
            except (TahunAjaran.DoesNotExist, MatkulKurikulum.DoesNotExist, Hari.DoesNotExist, SesiKuliah.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f"Error creating JadwalTawar (ID: {data['id']}): {e}. Make sure FK data exists."))
        self.stdout.write(self.style.SUCCESS('JadwalTawar data created/updated successfully.'))

        self.stdout.write("Creating KrsRecord data...")
        for data in dummy_data["KrsRecord"]:
            try:
                ta_obj = TahunAjaran.objects.get(kode=data['ta'])
                kdmk_obj = MatkulKurikulum.objects.get(kdmk=data['kdmk'])
                nim_dinus_obj = MahasiswaDinus.objects.get(nim_dinus=data['nim_dinus'])
                id_jadwal_obj = JadwalTawar.objects.get(id=data['id_jadwal']) if data['id_jadwal'] else None

                KrsRecord.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'ta': ta_obj,
                        'kdmk': kdmk_obj,
                        'id_jadwal': id_jadwal_obj,
                        'nim_dinus': nim_dinus_obj,
                        'sts': data['sts'],
                        'sks': data['sks'],
                        'modul': data['modul']
                    }
                )
            except (TahunAjaran.DoesNotExist, MatkulKurikulum.DoesNotExist, MahasiswaDinus.DoesNotExist, JadwalTawar.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f"Error creating KrsRecord (ID: {data['id']}): {e}. Make sure FK data exists."))
        self.stdout.write(self.style.SUCCESS('KrsRecord data created/updated successfully.'))

        self.stdout.write("Creating DaftarNilai data...")
        for data in dummy_data["DaftarNilai"]:
            try:
                nim_dinus_obj = MahasiswaDinus.objects.get(nim_dinus=data['nim_dinus'])
                kdmk_obj = MatkulKurikulum.objects.get(kdmk=data['kdmk'])
                DaftarNilai.objects.update_or_create(
                    nim_dinus=nim_dinus_obj,
                    kdmk=kdmk_obj,
                    defaults={
                        'nl': data['nl'],
                        'hide': data['hide']
                    }
                )
            except (MahasiswaDinus.DoesNotExist, MatkulKurikulum.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f"Error creating DaftarNilai for {data['nim_dinus']} and {data['kdmk']}: {e}. Make sure FK data exists."))
        self.stdout.write(self.style.SUCCESS('DaftarNilai data created/updated successfully.'))

        self.stdout.write("Creating ValidasiKrsMhs data...")
        for data in dummy_data["ValidasiKrsMhs"]:
            try:
                nim_dinus_obj = MahasiswaDinus.objects.get(nim_dinus=data['nim_dinus'])
                ta_obj = TahunAjaran.objects.get(kode=data['ta'])
                ValidasiKrsMhs.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'nim_dinus': nim_dinus_obj,
                        'job_date': parse_datetime(data['job_date']),
                        'job_host': data['job_host'],
                        'job_agent': data['job_agent'],
                        'ta': ta_obj
                    }
                )
            except (MahasiswaDinus.DoesNotExist, TahunAjaran.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f"Error creating ValidasiKrsMhs (ID: {data['id']}): {e}. Make sure FK data exists."))
        self.stdout.write(self.style.SUCCESS('ValidasiKrsMhs data created/updated successfully.'))

        self.stdout.write("Creating IPSemester data...")
        for data in dummy_data["IPSemester"]:
            try:
                ta_obj = TahunAjaran.objects.get(kode=data['ta'])
                nim_dinus_obj = MahasiswaDinus.objects.get(nim_dinus=data['nim_dinus'])
                IPSemester.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'ta': ta_obj,
                        'nim_dinus': nim_dinus_obj,
                        'sks': data['sks'],
                        'ips': data['ips'],
                        'last_update': parse_datetime(data['last_update'])
                    }
                )
            except (TahunAjaran.DoesNotExist, MahasiswaDinus.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f"Error creating IPSemester (ID: {data['id']}): {e}. Make sure FK data exists."))
        self.stdout.write(self.style.SUCCESS('IPSemester data created/updated successfully.'))


        self.stdout.write(self.style.SUCCESS('\nAll dummy data imported successfully!'))