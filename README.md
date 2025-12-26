<div align="center">

# 🏪 Toko Sembako Murah Jaya

### Sistem Informasi Manajemen Toko Sembako

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<p align="center">
  <strong>Aplikasi web untuk mengelola inventaris toko sembako dengan fitur CRUD lengkap, autentikasi, dan otorisasi berbasis role.</strong>
</p>

<p align="center">
  <a href="#-fitur">Fitur</a> •
  <a href="#-instalasi">Instalasi</a> •
  <a href="#-penggunaan">Penggunaan</a> •
  <a href="#-api-routes">API Routes</a> •
  <a href="#-deployment">Deployment</a>
</p>

---

### 📸 Screenshots

| Landing Page | Dashboard | Data Produk |
|:------------:|:---------:|:-----------:|
| ![Landing](https://via.placeholder.com/250x150/0d6efd/white?text=Landing+Page) | ![Dashboard](https://via.placeholder.com/250x150/198754/white?text=Dashboard) | ![Produk](https://via.placeholder.com/250x150/6c757d/white?text=Data+Produk) |

</div>

---

## 📖 Tentang Proyek

**Toko Sembako Murah Jaya** adalah sistem informasi berbasis web yang dibangun menggunakan Flask (Python) untuk mengelola operasional toko sembako. Sistem ini mendukung manajemen produk, kategori, dan pengguna dengan kontrol akses berbasis role.

Proyek ini dibuat sebagai tugas kuliah untuk mata kuliah Pemrograman Web dengan menerapkan konsep:
- **MVC Pattern** (Model-View-Controller)
- **CRUD Operations** (Create, Read, Update, Delete)
- **Authentication & Authorization**
- **Role-Based Access Control (RBAC)**

### 🎯 Tujuan
- Mempermudah pengelolaan inventaris produk sembako
- Menyediakan sistem autentikasi yang aman
- Memberikan akses berbeda untuk admin dan kasir
- Menyediakan dashboard informatif untuk monitoring stok

---

## ✨ Fitur

### 🔐 Autentikasi & Keamanan
| Fitur | Deskripsi |
|-------|-----------|
| **Login/Logout** | Sistem autentikasi dengan session management |
| **Register** | Pendaftaran user baru (default: role kasir) |
| **Password Hashing** | Enkripsi password menggunakan Werkzeug Scrypt |
| **Remember Me** | Opsi session persistent untuk kemudahan login |
| **Protected Routes** | Decorator `@login_required` dan `@admin_required` |

### 👥 Role-Based Access Control (RBAC)
| Fitur | Admin | Kasir |
|-------|:-----:|:-----:|
| Dashboard | ✅ | ✅ |
| Lihat Produk | ✅ | ✅ |
| Lihat Kategori | ✅ | ✅ |
| Tambah/Edit/Hapus Produk | ✅ | ❌ |
| Tambah/Edit/Hapus Kategori | ✅ | ❌ |
| Kelola User | ✅ | ❌ |

### 📦 Manajemen Data (CRUD)
| Entitas | Create | Read | Update | Delete |
|---------|:------:|:----:|:------:|:------:|
| **Kategori** | ✅ | ✅ | ✅ | ✅ (CASCADE) |
| **Produk** | ✅ | ✅ | ✅ | ✅ |
| **Users** | ✅ | ✅ | ✅ | ✅ |

> **Catatan**: Menghapus kategori akan otomatis menghapus semua produk yang terkait (ON DELETE CASCADE)

### 📊 Dashboard
- 📈 Total produk, kategori, dan user
- 📦 Total stok keseluruhan
- 🆕 Daftar 5 produk terbaru
- 📊 Statistik real-time

---

## 🗂️ Struktur Proyek

```
Toko Sembako/
│
├── 📁 .github/
│   └── copilot-instructions.md   # Instruksi untuk GitHub Copilot
│
├── 📁 database/
│   └── toko_sembako.sql          # Schema database MySQL/MariaDB
│
├── 📁 static/
│   └── styles.css                # Custom CSS styling
│
├── 📁 templates/
│   ├── index.html                # Landing page (public)
│   ├── login.html                # Halaman login
│   ├── register.html             # Halaman registrasi
│   ├── dashboard.html            # Dashboard utama
│   │
│   ├── read_kategori.html        # Daftar kategori
│   ├── create_kategori.html      # Form tambah kategori
│   ├── update_kategori.html      # Form edit kategori
│   │
│   ├── read_produk.html          # Daftar produk
│   ├── create_produk.html        # Form tambah produk
│   ├── update_produk.html        # Form edit produk
│   │
│   ├── read_user.html            # Daftar user (admin only)
│   ├── create_user.html          # Form tambah user (admin only)
│   └── update_user.html          # Form edit user (admin only)
│
├── app.py                        # Flask application & routes
├── models.py                     # Database models & CRUD operations
├── requirements.txt              # Python dependencies
└── README.md                     # Dokumentasi proyek (file ini)
```

---

## 📊 Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────┐              ┌─────────────────────────┐
│       KATEGORI          │              │         PRODUK          │
├─────────────────────────┤              ├─────────────────────────┤
│ id_kategori      (PK)   │◄────────────┐│ id_produk        (PK)   │
│ kode_kategori    (UQ)   │      1    N ││ kode_produk             │
│ nama_kategori           │             ││ nama                    │
│ deskripsi               │             ││ harga                   │
│ lokasi_rak              │             ││ stok                    │
└─────────────────────────┘             └│ kategori_id      (FK)   │
                                         └─────────────────────────┘
                                                    │
                                                    │ ON DELETE CASCADE
                                                    │ ON UPDATE CASCADE
                                                    ▼

┌─────────────────────────┐
│         USERS           │
├─────────────────────────┤
│ id_user          (PK)   │
│ username         (UQ)   │
│ role                    │  ← 'admin' | 'kasir'
│ password                │  ← Werkzeug Scrypt hash
└─────────────────────────┘
```

### Detail Tabel

<details>
<summary><strong>📁 Tabel: kategori</strong></summary>

| Kolom | Tipe Data | Constraint | Deskripsi |
|-------|-----------|------------|-----------|
| `id_kategori` | INT(11) | PRIMARY KEY, AUTO_INCREMENT | ID unik kategori |
| `kode_kategori` | VARCHAR(50) | NOT NULL, UNIQUE | Kode kategori (e.g., KAT001) |
| `nama_kategori` | VARCHAR(50) | NOT NULL | Nama kategori |
| `deskripsi` | TEXT | NOT NULL | Deskripsi kategori |
| `lokasi_rak` | VARCHAR(25) | NOT NULL | Lokasi rak penyimpanan |

</details>

<details>
<summary><strong>📦 Tabel: produk</strong></summary>

| Kolom | Tipe Data | Constraint | Deskripsi |
|-------|-----------|------------|-----------|
| `id_produk` | INT(11) | PRIMARY KEY, AUTO_INCREMENT | ID unik produk |
| `kode_produk` | VARCHAR(20) | NOT NULL | Kode produk (e.g., PRD001) |
| `nama` | VARCHAR(100) | NOT NULL | Nama produk |
| `harga` | INT(11) | NOT NULL | Harga dalam Rupiah |
| `stok` | INT(11) | NOT NULL, DEFAULT 0 | Jumlah stok tersedia |
| `kategori_id` | INT(11) | FOREIGN KEY | Referensi ke tabel kategori |

</details>

<details>
<summary><strong>👤 Tabel: users</strong></summary>

| Kolom | Tipe Data | Constraint | Deskripsi |
|-------|-----------|------------|-----------|
| `id_user` | INT(11) | PRIMARY KEY, AUTO_INCREMENT | ID unik user |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | Username untuk login |
| `role` | VARCHAR(25) | NOT NULL, DEFAULT 'kasir' | Role: admin atau kasir |
| `password` | VARCHAR(255) | NOT NULL | Password (Scrypt hash) |

</details>

---

## 🚀 Instalasi

### Prasyarat

Pastikan Anda sudah menginstall:
- ✅ **Python** 3.8 atau lebih tinggi
- ✅ **MySQL/MariaDB** 8.0+ (atau XAMPP/Laragon)
- ✅ **Git** (opsional, untuk clone repository)

### Langkah 1: Clone atau Download Repository

**Opsi A: Clone dengan Git**
```powershell
git clone https://github.com/username/toko-sembako.git
cd toko-sembako
```

**Opsi B: Download ZIP**
1. Klik tombol "Code" → "Download ZIP"
2. Ekstrak file ZIP ke folder yang diinginkan
3. Buka terminal di folder tersebut

### Langkah 2: Buat Virtual Environment

```powershell
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment (Windows PowerShell)
.\venv\Scripts\Activate

# Aktifkan virtual environment (Windows CMD)
venv\Scripts\activate.bat

# Aktifkan virtual environment (Linux/Mac)
source venv/bin/activate
```

> 💡 **Tips**: Anda akan melihat `(venv)` di awal command prompt jika berhasil

### Langkah 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Langkah 4: Setup Database

**Opsi A: Menggunakan phpMyAdmin (XAMPP/Laragon)**
1. Buka phpMyAdmin di browser (`http://localhost/phpmyadmin`)
2. Klik "New" untuk membuat database baru
3. Ketik nama: `toko_sembako` → klik "Create"
4. Pilih database `toko_sembako` → klik tab "Import"
5. Pilih file `database/toko_sembako.sql` → klik "Go"

**Opsi B: Menggunakan Command Line MySQL**
```powershell
# Login ke MySQL
mysql -u root -p

# Di dalam MySQL shell
source C:/path/to/database/toko_sembako.sql
```

### Langkah 5: Konfigurasi Database (Jika Diperlukan)

Jika konfigurasi database Anda berbeda, edit file `models.py`:

```python
class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",      # Ganti jika berbeda
            user="root",           # Ganti dengan username MySQL Anda
            password="",           # Ganti dengan password MySQL Anda
            db="toko_sembako",     # Nama database
            cursorclass=pymysql.cursors.DictCursor,
        )
```

### Langkah 6: Buat User Default

Untuk membuat user pertama, Anda bisa:

**Opsi A: Melalui Halaman Register**
1. Jalankan aplikasi (langkah 7)
2. Buka `/register` di browser
3. Daftarkan user baru (akan menjadi kasir)

**Opsi B: Langsung Insert ke Database**
```sql
-- Di phpMyAdmin atau MySQL shell
INSERT INTO users (username, role, password) VALUES 
('admin', 'admin', 'scrypt:32768:8:1$YOUR_HASH_HERE');
```

> ⚠️ **Penting**: Untuk password hash, gunakan Python:
> ```python
> from werkzeug.security import generate_password_hash
> print(generate_password_hash('password_anda'))
> ```

### Langkah 7: Jalankan Aplikasi

```powershell
python app.py
```

Output yang diharapkan:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Langkah 8: Akses Aplikasi

Buka browser dan kunjungi: **http://127.0.0.1:5000**

---

## 👤 Penggunaan

### Alur Penggunaan Sistem

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Landing   │────▶│    Login    │────▶│  Dashboard  │
│    Page     │     │   Page      │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │                   │                   ▼
       │                   │            ┌─────────────┐
       │                   │            │  Kelola     │
       ▼                   │            │  - Kategori │
┌─────────────┐            │            │  - Produk   │
│  Register   │────────────┘            │  - User     │
│  (Kasir)    │                         └─────────────┘
└─────────────┘
```

### Panduan untuk Admin

1. **Login** dengan akun admin
2. **Dashboard** - Lihat statistik toko
3. **Kelola Kategori** - Tambah, edit, hapus kategori produk
4. **Kelola Produk** - Tambah, edit, hapus produk
5. **Kelola User** - Tambah, edit, hapus user (admin/kasir)

### Panduan untuk Kasir

1. **Login** dengan akun kasir
2. **Dashboard** - Lihat statistik toko
3. **Lihat Kategori** - Melihat daftar kategori (read-only)
4. **Lihat Produk** - Melihat daftar produk (read-only)

---

## 🛣️ API Routes

### 🌐 Public Routes (Tanpa Login)

| Method | Endpoint | Deskripsi | Template |
|:------:|----------|-----------|----------|
| `GET` | `/` | Landing page | `index.html` |
| `GET` `POST` | `/login` | Halaman login | `login.html` |
| `GET` `POST` | `/register` | Halaman registrasi | `register.html` |
| `GET` | `/logout` | Logout & clear session | - |

### 🔒 Protected Routes (Login Required)

| Method | Endpoint | Deskripsi | Template |
|:------:|----------|-----------|----------|
| `GET` | `/dashboard` | Dashboard dengan statistik | `dashboard.html` |
| `GET` | `/kategori` | Daftar semua kategori | `read_kategori.html` |
| `GET` | `/produk` | Daftar semua produk | `read_produk.html` |

### 🔐 Admin Only Routes

| Method | Endpoint | Deskripsi | Template |
|:------:|----------|-----------|----------|
| `GET` `POST` | `/kategori/create` | Form tambah kategori | `create_kategori.html` |
| `GET` `POST` | `/kategori/update/<id>` | Form edit kategori | `update_kategori.html` |
| `GET` | `/kategori/delete/<id>` | Hapus kategori + produk terkait | - |
| `GET` `POST` | `/produk/create` | Form tambah produk | `create_produk.html` |
| `GET` `POST` | `/produk/update/<id>` | Form edit produk | `update_produk.html` |
| `GET` | `/produk/delete/<id>` | Hapus produk | - |
| `GET` | `/user` | Daftar semua user | `read_user.html` |
| `GET` `POST` | `/user/create` | Form tambah user | `create_user.html` |
| `GET` `POST` | `/user/update/<id>` | Form edit user | `update_user.html` |
| `GET` | `/user/delete/<id>` | Hapus user | - |

---

## 🔐 Keamanan

### Implementasi Keamanan

| Aspek | Implementasi | Status |
|-------|--------------|:------:|
| **Password Hashing** | Werkzeug Scrypt dengan salt | ✅ |
| **Session Security** | Flask secret key encryption | ✅ |
| **SQL Injection Prevention** | Parameterized queries | ✅ |
| **Input Validation** | Server-side validation | ✅ |
| **Access Control** | Decorator-based protection | ✅ |
| **Self-Delete Prevention** | User tidak bisa hapus diri sendiri | ✅ |

### Security Decorators

```python
@login_required      # Memastikan user sudah login
@admin_required      # Memastikan user adalah admin
```

### Contoh Penggunaan

```python
@app.route('/admin-only-page')
@admin_required  # Hanya admin yang bisa akses
def admin_page():
    return render_template('admin.html')
```

---

## 🛠️ Teknologi yang Digunakan

| Kategori | Teknologi | Versi |
|----------|-----------|:-----:|
| **Backend** | Python | 3.8+ |
| **Web Framework** | Flask | 3.0.0 |
| **Database** | MySQL/MariaDB | 8.0+ |
| **Database Driver** | PyMySQL | 1.1.0 |
| **Security** | Werkzeug | 3.0.1 |
| **Frontend CSS** | Bootstrap | 5.3.2 |
| **Icons** | Bootstrap Icons | 1.11.1 |
| **Template Engine** | Jinja2 | (included in Flask) |

---

## 📦 Dependencies

File `requirements.txt`:

```txt
Flask==3.0.0
PyMySQL==1.1.0
Werkzeug==3.0.1
```

### Install Semua Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🌐 Deployment

### Opsi 1: PythonAnywhere (Gratis & Mudah)

**Cocok untuk**: Demo, tugas kuliah, portfolio

1. Daftar gratis di [pythonanywhere.com](https://www.pythonanywhere.com)
2. Buka tab **"Files"** → Upload semua file proyek
3. Buka tab **"Databases"** → Buat MySQL database → Import `toko_sembako.sql`
4. Buka tab **"Web"** → Add new web app → Flask
5. Set **Source code** ke folder proyek Anda
6. Set **WSGI file** untuk mengarah ke `app.py`
7. Reload web app

**URL**: `https://username.pythonanywhere.com`

### Opsi 2: Railway (Memerlukan GitHub)

1. Push proyek ke GitHub
2. Login ke [railway.app](https://railway.app) dengan GitHub
3. New Project → Deploy from GitHub repo
4. Add MySQL Plugin
5. Set environment variables di Railway
6. Deploy otomatis setiap push

### Opsi 3: Local Network (Demo Lokal)

```powershell
# Jalankan agar bisa diakses dari jaringan lokal
python -c "from app import app; app.run(host='0.0.0.0', port=5000, debug=False)"
```

Akses dari device lain: `http://[IP_KOMPUTER]:5000`

---

## 🧪 Testing Manual

### Checklist Fungsionalitas

#### Autentikasi
- [ ] Register user baru → menjadi kasir
- [ ] Login dengan kredensial benar → redirect ke dashboard
- [ ] Login dengan kredensial salah → tampil pesan error
- [ ] Logout → session terhapus, redirect ke login
- [ ] Akses halaman protected tanpa login → redirect ke login

#### CRUD Kategori (Admin)
- [ ] Lihat daftar kategori
- [ ] Tambah kategori baru
- [ ] Edit kategori existing
- [ ] Hapus kategori → produk terkait ikut terhapus

#### CRUD Produk (Admin)
- [ ] Lihat daftar produk dengan nama kategori
- [ ] Tambah produk baru dengan pilih kategori
- [ ] Edit produk existing
- [ ] Hapus produk

#### CRUD User (Admin)
- [ ] Lihat daftar user
- [ ] Tambah user baru (admin/kasir)
- [ ] Edit user (username, role, password)
- [ ] Hapus user (tidak bisa hapus diri sendiri)

#### Role Access
- [ ] Kasir tidak bisa akses menu Create/Update/Delete
- [ ] Kasir akses URL admin → redirect dengan pesan error

---

## 📝 Changelog

### v1.0.0 (Desember 2025)

**🎉 Initial Release**

- ✅ Sistem autentikasi lengkap (login, logout, register)
- ✅ Role-based access control (admin & kasir)
- ✅ CRUD Kategori dengan cascade delete
- ✅ CRUD Produk dengan relasi ke kategori
- ✅ CRUD User (admin only)
- ✅ Dashboard dengan statistik real-time
- ✅ Responsive design dengan Bootstrap 5
- ✅ Flash messages untuk feedback user
- ✅ Error handlers untuk 404 dan 500

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Berikut cara berkontribusi:

1. **Fork** repository ini
2. **Clone** fork Anda ke lokal
3. **Buat branch** baru untuk fitur/fix Anda
   ```bash
   git checkout -b feature/nama-fitur
   ```
4. **Commit** perubahan Anda
   ```bash
   git commit -m "Menambahkan fitur X"
   ```
5. **Push** ke branch Anda
   ```bash
   git push origin feature/nama-fitur
   ```
6. Buat **Pull Request**

---

## ❓ FAQ

<details>
<summary><strong>Q: Kenapa muncul error "Access denied for user 'root'@'localhost'"?</strong></summary>

**A:** Password MySQL Anda salah. Edit `models.py` dan sesuaikan password:
```python
password="password_mysql_anda",
```
</details>

<details>
<summary><strong>Q: Bagaimana cara reset password admin?</strong></summary>

**A:** Jalankan di Python:
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('password_baru'))
```
Lalu update di database dengan hash yang dihasilkan.
</details>

<details>
<summary><strong>Q: Kenapa produk tidak muncul setelah kategori dihapus?</strong></summary>

**A:** Ini adalah fitur, bukan bug. Relasi menggunakan `ON DELETE CASCADE`, sehingga menghapus kategori akan menghapus semua produk yang terkait.
</details>

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License**.

```
MIT License

Copyright (c) 2025 Next-Gen Tech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

Lihat file [LICENSE](LICENSE) untuk detail lengkap.

---

## 👨‍💻 Author

<div align="center">

**Next-Gen Tech**

*Dibuat dengan ❤️ untuk tugas kuliah*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/username)

</div>

---

## 🙏 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap 5](https://getbootstrap.com/) - CSS framework
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library
- [PyMySQL](https://pymysql.readthedocs.io/) - MySQL driver for Python

---

<div align="center">

### ⭐ Jika proyek ini membantu, berikan bintang di GitHub! ⭐

**Made with ❤️ in Indonesia**

</div>
