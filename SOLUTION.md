# SOLUTION.md

## 📌 Ringkasan Solusi

Proyek ini merupakan implementasi REST API backend untuk sistem pengelolaan Kartu Rencana Studi (KRS) mahasiswa, sesuai dengan spesifikasi yang diminta dalam Technical Challenge BTIK UDINUS.

## 🗂️ Struktur Proyek

```
.
├── .coverage
├── .env.example
├── .gitignore
├── .pytest_cache/
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
├── AI-COLLABORATION.md
├── README.md
├── SOLUTION.md
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── api/
│   ├── apps.py
│   ├── management/
│   │   └── commands/
│   │       ├── dummy.json
│   │       └── seed_krs_data.py
│   ├── models.py
│   ├── serializers.py
│   ├── services/
│   │   └── services.py
│   ├── tests.py
│   ├── tests/
│   │   └── test_krs.py
│   ├── urls.py
│   ├── views.py
├── krs_api/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pytest.ini
└── requirements.txt
```

## 🔍 Arsitektur & Alur

1. **Mahasiswa mengakses data KRS saat ini** melalui endpoint:
   ```
   GET /api/v1/students/<nim>/krs/current/
   ```
   Mengembalikan semua mata kuliah yang sudah diambil di semester aktif.

2. **Menampilkan mata kuliah yang tersedia untuk ditambahkan ke KRS:**
   ```
   GET /api/v1/students/<nim>/courses/available/
   ```
   Melakukan pengecekan:
   - Apakah jadwal belum diambil?
   - Apakah tidak ada konflik bentrok sesi?

3. **Menambahkan mata kuliah ke KRS mahasiswa:**
   ```
   POST /api/v1/students/<nim>/krs/courses/
   ```
   Input: `id_jadwal`
   Validasi dilakukan di layer `services.py` sebelum data disimpan.

4. **Menghapus mata kuliah dari KRS mahasiswa:**
   ```
   DELETE /api/v1/students/<nim>/krs/courses/<id_jadwal>/
   ```

5. **Mengecek status KRS:**
   ```
   GET /api/v1/students/<nim>/krs/status/
   ```
   Output berupa:
   - Total SKS di semester aktif
   - Status validasi
   - IPS semester terakhir (jika tersedia)

## ✅ Testing

Semua endpoint diuji menggunakan `pytest` dalam file `test_krs.py`:
- Tes untuk semua skenario: ambil KRS, ambil mata kuliah tersedia, tambah & hapus jadwal, status KRS.
- Data dummy dibuat secara dinamis di dalam test menggunakan ORM.

## 🤝 Kolaborasi dengan AI

Lihat detail pada file [`AI-COLLABORATION.md`](./AI-COLLABORATION.md)
