# AI-COLLABORATION.md

## 📘 Tujuan

Dokumen ini menjelaskan secara jujur dan lengkap bagaimana AI (ChatGPT) digunakan sebagai asisten teknis selama pengembangan beberapa endpoint penting pada saat mengerjakan Technical Challenge BTIK UDINUS. Fokusnya pada proses CRUD (Create, Read, Update/Delete) terkait pengelolaan KRS mahasiswa.

---

## 🙋 Latar Belakang Pengembang

Saya, Rizki Afandi, menyatakan bahwa ini adalah **pengalaman pertama saya membangun REST API dengan CRUD lengkap menggunakan Django REST Framework**. Karena itu, saya banyak mengandalkan bantuan dari ChatGPT untuk:

- Memahami struktur REST API
- Menulis view berbasis class (APIView)
- Menangani model relasi banyak (FK)
- Mengatasi masalah yang muncul selama pengembangan
- Membuat test otomatis dengan `pytest` dan `APIClient`
- Membuat dokumentasi API dengan `drf-spectacular`
- MEmbuat Dokumentasi seperti `RREADME`, `SOLUTION`, DAN `AI-COLLABORATION`


Seluruh kode tetap saya tulis dan debug sendiri, namun AI digunakan secara intensif sebagai *coach* dan *code reviewer virtual*.

---

## Endpoint yang Dikembangkan Bersama AI

Berikut ini endpoint yang dibangun secara kolaboratif dengan bimbingan AI, dari nol hingga berhasil dites.

### 1. `/students/<str:nim>/courses/available/`
> Menampilkan mata kuliah yang **bisa diambil**, tidak bentrok dan belum pernah diambil.

**Peran AI:**
- Membantu logika filter `JadwalTawar` berbasis `hari`, `sesi`, dan pengecualian `KrsRecord`
- Menyarankan validasi input `nim`
- Membantu debugging ketika matkul yang sudah diambil masih muncul

---

### 2. `POST /students/<str:nim>/krs/courses/`
> Menambahkan mata kuliah ke KRS.

**Peran AI:**
- Menyarankan validasi ganda: jadwal tidak bentrok, belum pernah diambil, masih open
- Menyarankan struktur response JSON agar informatif

---

### 3. `DELETE /students/<str:nim>/krs/courses/<str:id_jadwal>/`
> Menghapus matkul dari KRS, selama belum tervalidasi.

**Peran AI:**
- Membantu mengenali bug ketika URL pattern tidak cocok
- Menyarankan response `200 OK` dengan pesan konfirmasi

---

### 4. `GET /students/<str:nim>/krs/status/`
> Menampilkan status KRS mahasiswa: apakah tervalidasi, total SKS, dan IPS semester sebelumnya.

**Peran AI:**
- Menjelaskan cara agregasi data dari 3 model berbeda
- Menyusun struktur service function dan serializer
- Menyederhanakan test case verifikasi SKS dan IPS

---

## 🧪 Testing

AI membantu saya menyusun dan menyatukan beberapa skenario test menjadi satu function `test_krs`, yang menguji:

- GET data KRS aktif
- GET matkul yang tersedia
- POST tambah matkul baru
- DELETE matkul
- GET status KRS setelah perubahan

---

## 🧾 Penutup

Sebagai peserta pemula dalam pengembangan backend REST API, saya mengakui bahwa **AI sangat membantu saya melewati banyak hambatan teknis**. Namun saya juga memastikan bahwa:

- Saya benar-benar memahami alur kode yang saya tulis
- Saya melakukan debugging dan validasi hasil secara manual
- Semua pengujian dijalankan sendiri, bukan hanya disalin

Dengan demikian, hasil akhir tetap mencerminkan proses belajar aktif dan usaha pribadi, bukan hasil otomatis sepenuhnya.

---

### 👤 Penulis

Rizki Afandi  
Peserta Backend Challenge – BTIK UDINUS  
17 Juli 2025
