from rest_framework import serializers
from app.models import MahasiswaDinus, MatkulKurikulum, Hari, JadwalTawar, SesiKuliah, TahunAjaran, KrsRecord,ValidasiKrsMhs,IPSemester

class MahasiswaDinusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MahasiswaDinus
        fields = ['nim_dinus', 'ta_masuk']  

class MatkulKurikulumSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatkulKurikulum
        fields = ['kdmk', 'nmmk', 'nmen', 'tp', 'sks']

class HariSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hari
        fields = ['nama', 'nama_en']

class SesiKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesiKuliah
        fields = ['jam', 'sks', 'jam_mulai', 'jam_selesai', 'status']

class JadwalTawarSerializer(serializers.ModelSerializer):
    id_hari1 = HariSerializer()
    id_hari2 = HariSerializer()
    id_hari3 = HariSerializer()
    id_sesi1 = SesiKuliahSerializer()
    id_sesi2 = SesiKuliahSerializer()
    id_sesi3 = SesiKuliahSerializer()

    class Meta:
        model = JadwalTawar
        fields = ['ta', 'kdmk', 'klpk', 'klpk_2', 'kdds', 'kdds2', 'jmax', 'jsisa',
                  'id_hari1', 'id_hari2', 'id_hari3', 'id_sesi1', 'id_sesi2', 
                  'id_sesi3', 'id_ruang1', 'id_ruang2', 'id_ruang3', 
                  'jns_jam', 'open_class']


class TahunAjaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = TahunAjaran
        fields = ['ta', 'nama', 'aktif']

class KrsRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KrsRecord
        fields = ['ta', 'kdmk', 'id_jadwal', 'nim_dinus', 'sts', 'sks', 'modul']
        depth = 1
        extra_kwargs = {
            'id': {'read_only': True},  # Ini penting
        }

class KrsStatusSerializer(serializers.Serializer):
    validated = serializers.BooleanField()
    total_sks = serializers.IntegerField()
    ips_last_semester = serializers.CharField(allow_null=True)

