# Toko Sembako Murah Jaya - Copilot Instructions

## Project Overview
Sistem Informasi Toko Sembako berbasis Flask untuk tugas kuliah. Website ini mengelola produk sembako dengan fitur CRUD, autentikasi, dan otorisasi berbasis role (admin/kasir).

## Architecture

### File Structure
```
app.py          # Flask routes dan controllers
models.py       # Semua operasi database (CRUD functions)
templates/      # Jinja2 HTML templates
static/         # CSS files (styles.css)
```

### Database (MariaDB: `toko_sembako`)
- **kategori**: id_kategori, kode_kategori, nama_kategori, deskripsi, lokasi_rak
- **produk**: id_produk, kode_produk, nama, harga, stok, kategori_id (FK → kategori)
- **users**: id_user, username, role, password (hashed)

Relasi: `produk.kategori_id` → `kategori.id_kategori`

## Conventions

### Backend (Python/Flask)
- Semua operasi database ditulis di `models.py` sebagai functions terpisah
- Import functions dari `models.py` ke `app.py`, bukan akses database langsung
- Password hashing menggunakan `werkzeug.security` (generate_password_hash, check_password_hash)
- Session keys: `user_id`, `username`, `role`
- Flash messages menggunakan kategori Bootstrap: `success`, `danger`, `warning`, `info`

### Frontend (HTML/CSS)
- Gunakan Bootstrap 5.3.2 + Bootstrap Icons 1.11.1 via CDN
- Custom CSS di `static/styles.css` - minimize usage, leverage Bootstrap
- Color palette: Biru (--primary-color: #0d6efd)
- Template pattern: Include navbar, content sections, footer
- Gunakan Jinja2 `url_for()` untuk static files dan routes
- Bahasa Indonesia untuk UI text

### CSS Guidelines
- Gunakan CSS variables di `:root` untuk warna
- Prefer Bootstrap classes, custom CSS hanya jika diperlukan
- Keep CSS under 200 lines
- Simple animations: fadeInUp, hover effects

## Key Patterns

### Route Protection
```python
if 'user_id' not in session:
    flash('Silakan login terlebih dahulu.', 'danger')
    return redirect(url_for('login'))
```

### Flash Messages in Templates
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}
```

### Database Function Pattern (models.py)
```python
def get_entity_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM table WHERE id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
```

## Running the Application
```powershell
# Activate virtual environment first
python app.py
# Access at http://127.0.0.1:5000
```

## Role-Based Access
- **admin**: Full CRUD access untuk semua tabel
- **kasir**: Read-only atau limited access (to be implemented)
