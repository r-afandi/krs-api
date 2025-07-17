
# 🎓 KRS API – Backend Technical Challenge BTIK UDINUS

Sebuah REST API untuk sistem pengelolaan Kartu Rencana Studi (KRS) mahasiswa berbasis Django REST Framework. Proyek ini merupakan bagian dari Technical Challenge BTIK Universitas Dian Nuswantoro (UDINUS).

---

## 🚀 Fitur Utama

- Menampilkan KRS aktif mahasiswa
- Menampilkan mata kuliah yang tersedia dan tidak bentrok
- Menambahkan dan menghapus mata kuliah ke/dari KRS
- Menampilkan status KRS (validasi, total SKS, IPS)

---

## 🧑‍💻 Teknologi

- **Python 3.12**
- **Django 5.2.4**
- **Django REST Framework**
- **PostgreSQL (disarankan)**
- **Pytest + APIClient** untuk pengujian otomatis

---

## 🗂️ Struktur Endpoint

| Endpoint | Method | Deskripsi |
|---------|--------|----------|
| `/students/<nim>/krs/current/` | GET | KRS aktif mahasiswa |
| `/students/<nim>/courses/available/` | GET | Matkul tersedia (belum diambil, tidak bentrok) |
| `/students/<nim>/krs/courses/` | POST | Tambahkan matkul ke KRS |
| `/students/<nim>/krs/courses/<id_jadwal>/` | DELETE | Hapus matkul dari KRS |
| `/students/<nim>/krs/status/` | GET | Status KRS: validasi, total SKS, IPS |

---

## ⚙️ Cara Menjalankan

### 1. Clone Repo
```bash
git clone https://github.com/r-afandi/krs-api
cd krs-api
```

### 2. Buat Virtual Environment
```bash
python -m venv .venv
. .venv\Scripts\activate

```

### 3. Install Dependency
```bash
pip install -r requirements.txt
```

### 4. Migrasi Database (WINDOWS)
```bash
python manage.py migrate
python manage.py seed_krs_data
python manage.py makemigration
python manage.py migrate
```

### 5. Jalankan Server
```bash
python manage.py runserver
```

---

## 🧪 Jalankan Testing

```bash
pytest -s
```

Contoh hasil output:
```
================================================= 1 passed in 13.17s ==================================================
```

---

## 📁 File Penting

| File | Fungsi |
|------|--------|
| `README.md` | Dokumentasi setup dan overview |
| `SOLUTION.md` | Penjelasan teknologi yang digunakan |
| `AI-COLLABORATION.md` | Dokumentasi kontribusi AI (ChatGPT) |
| `test_krs.py` | Test endpoint utama |
| `service.py` | Logika utama pemrosesan bisnis |
| `views.py` | Endpoint API |
| `serializers.py` | Serialisasi objek database ke JSON |

---

## 👤 Developer

**Rizki Afandi**  
  
Juli 2025



