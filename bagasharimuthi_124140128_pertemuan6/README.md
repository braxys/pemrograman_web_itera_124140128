# Pertemuan 6 — Pyramid Framework (RESTful API Mahasiswa & Matakuliah)

## Identitas Praktikan

- **Nama Lengkap:** Bagas Hari Muthi
- **NIM:** 124140128
- **Kelas Praktikum:** RB

## Deskripsi Aplikasi

Aplikasi RESTful API berbasis **Pyramid Framework**, **SQLAlchemy ORM**, **Alembic**, dan **PostgreSQL** untuk mengelola data **Mahasiswa** dan **Matakuliah**.

Fitur utama:
- Operasi CRUD lengkap (Create, Read All, Read One, Update, Delete) untuk resource **Mahasiswa** (`/api/mahasiswa`) dan **Matakuliah** (`/api/matakuliah`).
- Validasi payload JSON, validasi nilai `sks` dan `semester` agar berupa bilangan bulat positif (`> 0`), serta penanganan keunikan `nim` dan `kode_mk`.
- Pengembalian status HTTP standar (`200 OK`, `400 Bad Request`, `404 Not Found`).
- Manajemen skema tabel menggunakan migrasi Alembic dan seeding data awal melalui `initialize_db.py`.

## Struktur Direktori

```text
bagasharimuthi_124140128_pertemuan6/
├── development.ini
├── production.ini
├── setup.py
├── README.md
├── .gitignore
├── screenshot/
│   ├── endpoint-mhs.png
│   └── endpoint-matkul.png
└── pyramid_mahasiswa/
    ├── __init__.py
    ├── routes.py
    ├── tests.py
    ├── alembic/
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions/
    │       ├── 20261125_adc9d3c7ffc1.py   # create mahasiswa table
    │       └── 20261125_5d68b4e08b0c.py   # create matakuliah table
    ├── models/
    │   ├── __init__.py
    │   ├── meta.py
    │   ├── mymodel.py
    │   ├── mahasiswa.py
    │   └── matakuliah.py
    ├── scripts/
    │   ├── __init__.py
    │   └── initialize_db.py
    └── views/
        ├── __init__.py
        ├── default.py
        ├── notfound.py
        ├── mahasiswa.py
        └── matakuliah.py
```

## Instalasi & Menjalankan Server

### 1. Persiapan Virtual Environment & Dependensi

```powershell
cd bagasharimuthi_124140128_pertemuan6
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip setuptools
pip install -e ".[testing]"
```

### 2. Konfigurasi Database PostgreSQL

Masuk ke `psql` sebagai user `postgres` lalu buat database dan user aplikasi:

```sql
CREATE DATABASE pyramid_mahasiswa;
CREATE USER pyramid_user WITH ENCRYPTED PASSWORD 'pyramid_pass';
GRANT ALL PRIVILEGES ON DATABASE pyramid_mahasiswa TO pyramid_user;
\c pyramid_mahasiswa
GRANT ALL ON SCHEMA public TO pyramid_user;
\q
```

Pastikan `sqlalchemy.url` pada `development.ini` sudah mengarah ke database PostgreSQL:

```ini
sqlalchemy.url = postgresql+psycopg2://pyramid_user:pyramid_pass@localhost:5432/pyramid_mahasiswa
```

### 3. Migrasi Alembic & Seeding Data Awal

```powershell
alembic -c development.ini upgrade head
python -m pyramid_mahasiswa.scripts.initialize_db development.ini
```

### 4. Menjalankan Server Development

```powershell
pserve development.ini --reload
```

Server berjalan di `http://localhost:6543`.

### 5. Menjalankan Unit & Functional Test

```powershell
pytest -v
```

## Daftar Endpoint REST API

### Mahasiswa

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| `GET` | `/api/mahasiswa` | Mengambil seluruh daftar mahasiswa |
| `GET` | `/api/mahasiswa/{id}` | Mengambil detail mahasiswa berdasarkan `id` |
| `POST` | `/api/mahasiswa` | Menambahkan data mahasiswa baru (`nim`, `nama`, `jurusan` wajib) |
| `PUT` | `/api/mahasiswa/{id}` | Memperbarui data mahasiswa berdasarkan `id` |
| `DELETE` | `/api/mahasiswa/{id}` | Menghapus data mahasiswa berdasarkan `id` |

### Matakuliah

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| `GET` | `/api/matakuliah` | Mengambil seluruh daftar matakuliah |
| `GET` | `/api/matakuliah/{id}` | Mengambil detail matakuliah berdasarkan `id` |
| `POST` | `/api/matakuliah` | Menambahkan matakuliah baru (`kode_mk`, `nama_mk`, `sks`, `semester` wajib; `sks` & `semester` > 0) |
| `PUT` | `/api/matakuliah/{id}` | Memperbarui data matakuliah berdasarkan `id` |
| `DELETE` | `/api/matakuliah/{id}` | Menghapus data matakuliah berdasarkan `id` |

## Pengujian Endpoint (cURL)

### 1. Endpoint Mahasiswa

```powershell
# GET ALL (200)
curl.exe -X GET http://localhost:6543/api/mahasiswa

# GET ONE (200)
curl.exe -X GET http://localhost:6543/api/mahasiswa/1

# POST CREATE (200)
'{"nim":"124140128","nama":"Bagas Hari Muthi","jurusan":"Teknik Informatika","tanggal_lahir":"2005-01-15","alamat":"Bandar Lampung"}' | curl.exe -X POST http://localhost:6543/api/mahasiswa -H "Content-Type: application/json" --data-binary "@-"

# POST VALIDATION ERROR (400)
'{"nama":"Tanpa NIM","jurusan":"Teknik Informatika"}' | curl.exe -X POST http://localhost:6543/api/mahasiswa -H "Content-Type: application/json" --data-binary "@-"

# PUT UPDATE (200)
'{"jurusan":"Teknik Informatika","alamat":"Lampung Selatan"}' | curl.exe -X PUT http://localhost:6543/api/mahasiswa/3 -H "Content-Type: application/json" --data-binary "@-"

# DELETE (200)
curl.exe -X DELETE http://localhost:6543/api/mahasiswa/3

# GET NOT FOUND (404)
curl.exe -X GET http://localhost:6543/api/mahasiswa/3
```

### 2. Endpoint Matakuliah

```powershell
# GET ALL (200)
curl.exe -X GET http://localhost:6543/api/matakuliah

# GET ONE (200)
curl.exe -X GET http://localhost:6543/api/matakuliah/1

# POST CREATE (200)
'{"kode_mk":"IF25-31001","nama_mk":"Kecerdasan Buatan","sks":3,"semester":5}' | curl.exe -X POST http://localhost:6543/api/matakuliah -H "Content-Type: application/json" --data-binary "@-"

# POST MISSING FIELD (400)
'{"kode_mk":"IF25-99999","nama_mk":"Kosong"}' | curl.exe -X POST http://localhost:6543/api/matakuliah -H "Content-Type: application/json" --data-binary "@-"

# POST NEGATIVE SKS (400)
'{"kode_mk":"IF25-99999","nama_mk":"SKS Negatif","sks":-1,"semester":3}' | curl.exe -X POST http://localhost:6543/api/matakuliah -H "Content-Type: application/json" --data-binary "@-"

# PUT UPDATE (200)
'{"nama_mk":"Kecerdasan Buatan Lanjut","sks":4}' | curl.exe -X PUT http://localhost:6543/api/matakuliah/4 -H "Content-Type: application/json" --data-binary "@-"

# DELETE (200)
curl.exe -X DELETE http://localhost:6543/api/matakuliah/4

# GET NOT FOUND (404)
curl.exe -X GET http://localhost:6543/api/matakuliah/4
```

## Hasil Pengujian API

### Output cURL Mahasiswa

```text
GET /api/mahasiswa -> 200
{"mahasiswas": [{"id": 1, "nim": "124140212", "nama": "Arya Dimar Fath", "jurusan": "Teknik Informatika", "tanggal_lahir": "2005-04-12", "alamat": "Bandar Lampung"}, {"id": 2, "nim": "124140008", "nama": "MAULANA MUHAMMAD RIZKI", "jurusan": "Teknik Informatika", "tanggal_lahir": "2005-07-20", "alamat": "Lampung Selatan"}]}

GET /api/mahasiswa/1 -> 200
{"mahasiswa": {"id": 1, "nim": "124140212", "nama": "Arya Dimar Fath", "jurusan": "Teknik Informatika", "tanggal_lahir": "2005-04-12", "alamat": "Bandar Lampung"}}

POST /api/mahasiswa -> 200
{"success": true, "mahasiswa": {"id": 3, "nim": "124140128", "nama": "Bagas Hari Muthi", "jurusan": "Teknik Informatika", "tanggal_lahir": "2005-01-15", "alamat": "Bandar Lampung"}}

POST /api/mahasiswa (tanpa nim) -> 400
{"error":"Field nim wajib diisi!"}

PUT /api/mahasiswa/3 -> 200
{"success": true, "mahasiswa": {"id": 3, "nim": "124140128", "nama": "Bagas Hari Muthi", "jurusan": "Teknik Informatika", "tanggal_lahir": "2005-01-15", "alamat": "Lampung Selatan"}}

DELETE /api/mahasiswa/3 -> 200
{"success": true, "message": "Mahasiswa dengan ID 3 berhasil dihapus"}

GET /api/mahasiswa/3 -> 404
{"error":"Mahasiswa dengan ID 3 tidak ditemukan"}
```

### Output cURL Matakuliah

```text
GET /api/matakuliah -> 200
{"matakuliahs": [{"id": 1, "kode_mk": "IF25-22015", "nama_mk": "Sistem Informasi", "sks": 3, "semester": 4}, {"id": 2, "kode_mk": "IF25-22014", "nama_mk": "Pengembangan Aplikasi Web", "sks": 3, "semester": 4}, {"id": 3, "kode_mk": "IF25-21008", "nama_mk": "Jaringan Komputer", "sks": 3, "semester": 3}]}

GET /api/matakuliah/1 -> 200
{"matakuliah": {"id": 1, "kode_mk": "IF25-22015", "nama_mk": "Sistem Informasi", "sks": 3, "semester": 4}}

POST /api/matakuliah -> 200
{"success": true, "matakuliah": {"id": 4, "kode_mk": "IF25-31001", "nama_mk": "Kecerdasan Buatan", "sks": 3, "semester": 5}}

POST /api/matakuliah (field tidak lengkap) -> 400
{"error":"Field sks wajib diisi!"}

POST /api/matakuliah (sks <= 0) -> 400
{"error":"Field sks harus berupa bilangan bulat positif (> 0)"}

PUT /api/matakuliah/4 -> 200
{"success": true, "matakuliah": {"id": 4, "kode_mk": "IF25-31001", "nama_mk": "Kecerdasan Buatan Lanjut", "sks": 4, "semester": 5}}

DELETE /api/matakuliah/4 -> 200
{"success": true, "message": "Matakuliah dengan ID 4 berhasil dihapus"}

GET /api/matakuliah/4 -> 404
{"error":"Matakuliah dengan ID 4 tidak ditemukan"}
```

## Tangkapan Layar Pengujian

### 1. Pengujian Endpoint Mahasiswa

![Pengujian Endpoint Mahasiswa](screenshot/endpoint-mhs.png)

### 2. Pengujian Endpoint Matakuliah

![Pengujian Endpoint Matakuliah](screenshot/endpoint-matkul.png)
