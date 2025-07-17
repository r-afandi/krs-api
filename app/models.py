from django.db import models

class TahunAjaran(models.Model):
    kode = models.CharField(max_length=255, unique=True, null=True, blank=True)
    tahun_akhir = models.CharField(max_length=255, null=True, blank=True)
    tahun_awal = models.CharField(max_length=255, null=True, blank=True)
    
    # 1 = reg ganjil, 2 = reg genap, 3 = sp ganjil, 4 = sp genap
    JNS_SMT_CHOICES = [
        (1, 'Reguler Ganjil'),
        (2, 'Reguler Genap'),
        (3, 'SP Ganjil'),
        (4, 'SP Genap'),
    ]
    jns_smt = models.IntegerField(choices=JNS_SMT_CHOICES,null=True, blank=True)
    
    set_aktif = models.BooleanField(null=True, blank=True)
    
    # 1 = spp; 2 = sks; 3 = kekurangan
    BUKU_TAGIH_CHOICES = [
        (1, 'SPP'),
        (2, 'SKS'),
        (3, 'Kekurangan'),
    ]
    buku_tagih_jenis = models.PositiveSmallIntegerField(choices=BUKU_TAGIH_CHOICES, default=0)

    update_time = models.DateTimeField(null=True, blank=True)
    update_id = models.CharField(max_length=18, null=True, blank=True)
    update_host = models.CharField(max_length=18, null=True, blank=True)
    added_time = models.DateTimeField(null=True, blank=True)
    added_id = models.CharField(max_length=18, null=True, blank=True)
    added_host = models.CharField(max_length=18, null=True, blank=True)
    tgl_masuk = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.kode} ({self.tahun_awal}/{self.tahun_akhir})"    
    class Meta:
        db_table = 'tahun_ajaran'

class MahasiswaDinus(models.Model):
    nim_dinus = models.CharField(max_length=50, unique=True, primary_key=True)
    ta_masuk = models.IntegerField(null=True, blank=True)
    prodi = models.CharField(max_length=5, null=True, blank=True)
    pass_mhs = models.CharField(max_length=128, null=True, blank=True)
    kelas = models.IntegerField()
    akdm_stat = models.CharField(max_length=2)

    class Meta:
        db_table = 'mahasiswa_dinus'


class MatkulKurikulum(models.Model):
    kdmk = models.CharField(max_length=255,primary_key=True)
    nmmk = models.CharField(max_length=255)
    nmen = models.CharField(max_length=255, null=True, blank=True)
    tp = models.CharField(max_length=2, choices=[('T', 'Teori'), ('P', 'Praktik'), ('TP', 'Teori dan Praktik')])
    sks = models.IntegerField()
    sks_t = models.SmallIntegerField()
    sks_p = models.SmallIntegerField()
    smt = models.IntegerField()
    jns_smt = models.IntegerField()
    aktif = models.BooleanField()
    kur_nama = models.CharField(max_length=255, null=True, blank=True)
    kelompok_makul = models.CharField(max_length=3, choices=[('MPK', 'MPK'), ('MKK', 'MKK'), ('MKB', 'MKB'), ('MKD', 'MKD'), ('MBB', 'MBB'), ('MPB', 'MPB')])
    kur_aktif = models.BooleanField()
    jenis_matkul = models.CharField(max_length=7, choices=[('wajib', 'Wajib'), ('pilihan', 'Pilihan')])

    class Meta:
        db_table = 'matkul_kurikulum'
class Hari(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=6)
    nama_en = models.CharField(max_length=20)

    class Meta:
        db_table = 'hari'

from django.db import models

class Ruang(models.Model):
    nama = models.CharField(max_length=250)
    nama2 = models.CharField(max_length=250, default='-')
    id_jenis_makul = models.IntegerField(null=True, blank=True)
    id_fakultas = models.CharField(max_length=5, null=True, blank=True)
    kapasitas = models.PositiveSmallIntegerField(default=0)
    kap_ujian = models.PositiveSmallIntegerField(default=0)
    
    # 1: buka, 0: tutup, 2: hapus
    STATUS_CHOICES = [
        (0, 'Tutup'),
        (1, 'Buka'),
        (2, 'Hapus'),
    ]
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    
    luas = models.CharField(max_length=5, default='0', help_text='meter persegi')
    kondisi = models.CharField(max_length=50, null=True, blank=True)
    jumlah = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nama

    class Meta:
        db_table = 'ruang'

class SesiKuliah(models.Model):
    id = models.AutoField(primary_key=True)
    jam = models.CharField(max_length=11)
    sks = models.SmallIntegerField()
    jam_mulai = models.TimeField(null=True, blank=True)
    jam_selesai = models.TimeField(null=True, blank=True)
    status = models.IntegerField()

    class Meta:
        db_table = 'sesi_kuliah'
class SesiKuliahBentrok(models.Model):
    id = models.AutoField(primary_key=True)
    sesi_bentrok= models.ForeignKey(SesiKuliah, on_delete=models.CASCADE, db_column='id_bentrok', related_name='bentrok')
    sesi_bentrok_dengan = models.ForeignKey(SesiKuliah, on_delete=models.CASCADE, db_column='id_bentrok_dengan', related_name='bentrok_with')

    class Meta:
        db_table = 'sesi_kuliah_bentrok'
        
class JadwalTawar(models.Model):
    id = models.AutoField(primary_key=True)
    ta = models.ForeignKey(TahunAjaran, to_field='kode', on_delete=models.CASCADE, db_column='ta')
    kdmk = models.ForeignKey(MatkulKurikulum, on_delete=models.CASCADE, db_column='kdmk')
    klpk = models.CharField(max_length=15)
    klpk_2 = models.CharField(max_length=15, null=True, blank=True)
    kdds = models.IntegerField()
    kdds2 = models.IntegerField(null=True, blank=True)
    jmax = models.IntegerField(default=0)
    jsisa = models.IntegerField(default=0)
    id_hari1 = models.ForeignKey(Hari, on_delete=models.CASCADE, db_column='id_hari1', related_name='jadwal_hari1', null=True, blank=True)
    id_hari2 = models.ForeignKey(Hari, on_delete=models.CASCADE, db_column='id_hari2', related_name='jadwal_hari2', null=True, blank=True)
    id_hari3 = models.ForeignKey(Hari, on_delete=models.CASCADE, db_column='id_hari3', related_name='jadwal_hari3', null=True, blank=True)
    id_sesi1 = models.ForeignKey(SesiKuliah, on_delete=models.CASCADE, db_column='id_sesi1', related_name='jadwal_sesi1', default=0,null=True, blank=True)
    id_sesi2 = models.ForeignKey(SesiKuliah, on_delete=models.CASCADE, db_column='id_sesi2', related_name='jadwal_sesi2', default=0, null=True, blank=True)
    id_sesi3 = models.ForeignKey(SesiKuliah, on_delete=models.CASCADE, db_column='id_sesi3', related_name='jadwal_sesi3',default=0, null=True, blank=True)
    id_ruang1 = models.IntegerField()
    id_ruang2 = models.IntegerField()
    id_ruang3 = models.IntegerField()
    jns_jam = models.IntegerField()
    open_class = models.BooleanField(default=True)

    class Meta:
        db_table = 'jadwal_tawar'

class KrsRecord(models.Model):
    id = models.AutoField(primary_key=True)
    ta = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE, db_column='ta')
    kdmk = models.ForeignKey(MatkulKurikulum, on_delete=models.CASCADE, db_column='kdmk')
    id_jadwal = models.ForeignKey(JadwalTawar, on_delete=models.CASCADE, db_column='id_jadwal',null=True)
    nim_dinus = models.ForeignKey(MahasiswaDinus, on_delete=models.CASCADE, db_column='nim_dinus')
    sts = models.CharField(max_length=1, choices=[('A', 'Aktif'), ('T', 'Tidak Aktif')],null=True)
    sks = models.IntegerField(null=True, blank=True)
    modul = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'krs_record'

class DaftarNilai(models.Model):
    nim_dinus = models.ForeignKey(MahasiswaDinus, on_delete=models.CASCADE, db_column='nim_dinus')
    kdmk = models.ForeignKey(MatkulKurikulum, on_delete=models.CASCADE, db_column='kdmk')
    nl = models.CharField(max_length=2, null=True, blank=True)
    hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'daftar_nilai'

class ValidasiKrsMhs(models.Model):
    id = models.AutoField(primary_key=True)
    nim_dinus = models.ForeignKey(MahasiswaDinus, on_delete=models.CASCADE, db_column='nim_dinus')
    job_date = models.DateTimeField(null=True, blank=True)
    job_host = models.CharField(max_length=255, null=True, blank=True)
    job_agent = models.CharField(max_length=255, null=True, blank=True)
    ta = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE, db_column='ta')

    class Meta:
        db_table = 'validasi_krs_mhs'
class IPSemester(models.Model):
    id = models.AutoField(primary_key=True)
    ta = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE, db_column='ta')
    nim_dinus = models.ForeignKey(MahasiswaDinus, on_delete=models.CASCADE, db_column='nim_dinus')
    sks = models.IntegerField()
    ips = models.CharField(max_length=5)
    last_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'ip_semester'