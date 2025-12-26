"""
==============================================
Flask Application - Toko Sembako Murah Jaya
==============================================

Sistem Informasi Manajemen Toko Sembako
dengan fitur CRUD, autentikasi, dan otorisasi berbasis role.

==============================================
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from models import User, Produk, Kategori

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ============================================================
# FLASK APPLICATION SETUP
# ============================================================

app = Flask(__name__)

# Secret key untuk session (ambil dari environment atau gunakan default)
app.secret_key = os.getenv('SECRET_KEY', 'toko_sembako_secret_key_2025_change_in_production')

# Konfigurasi session
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ============================================================
# DECORATOR UNTUK AUTENTIKASI DAN OTORISASI
# ============================================================

def login_required(f):
    """Decorator untuk memastikan user sudah login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator untuk memastikan user adalah admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'danger')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Anda tidak memiliki akses untuk halaman ini.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================
# CONTEXT PROCESSOR - Untuk menyediakan data ke semua template
# ============================================================

@app.context_processor
def inject_user():
    """Menyediakan informasi user ke semua template"""
    return {
        'current_user': {
            'is_authenticated': 'user_id' in session,
            'username': session.get('username'),
            'role': session.get('role'),
            'is_admin': session.get('role') == 'admin'
        }
    }

# ============================================================
# ROUTE UTAMA
# ============================================================

@app.route('/')
def index():
    """Halaman landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Halaman dashboard setelah login"""
    # Ambil statistik untuk dashboard
    produk_list = Produk.get_all_produk()
    kategori_list = Kategori.get_all_kategori()
    user_list = User.get_all_users() if session.get('role') == 'admin' else []
    
    stats = {
        'total_produk': len(produk_list) if produk_list else 0,
        'total_kategori': len(kategori_list) if kategori_list else 0,
        'total_user': len(user_list) if user_list else 0,
        'total_stok': sum([p['stok'] for p in produk_list]) if produk_list else 0
    }
    
    return render_template('dashboard.html', stats=stats, produk_terbaru=produk_list[:5] if produk_list else [])

# ============================================================
# AUTENTIKASI - Login, Logout, Register
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Halaman login dengan autentikasi"""
    # Jika sudah login, redirect ke dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember')  # Checkbox "ingat saya"
        
        # Validasi input
        if not username or not password:
            flash('Username dan password harus diisi.', 'warning')
            return render_template('login.html')
        
        # Cek kredensial
        user = User.check_login(username, password)
        if user:
            # Set session
            session['user_id'] = user['id_user']
            session['username'] = user['username']
            session['role'] = user['role']
            
            # Jika "ingat saya" dicentang, perpanjang session
            if remember:
                session.permanent = True
            
            flash(f'Selamat datang, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout dan hapus session"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Sampai jumpa, {username}! Anda telah keluar dari sistem.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Halaman registrasi user baru (hanya kasir)"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validasi input
        if not username or not password:
            flash('Semua field harus diisi.', 'warning')
            return render_template('register.html')
        
        if len(password) < 4:
            flash('Password minimal 4 karakter.', 'warning')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'danger')
            return render_template('register.html')
        
        # Cek apakah username sudah ada
        try:
            User.create_user(username, password, 'kasir')  # Default role: kasir
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Username sudah digunakan. Silakan pilih username lain.', 'danger')
    
    return render_template('register.html')

# ============================================================
# CRUD KATEGORI
# ============================================================

@app.route('/kategori')
@login_required
def read_kategori():
    """Menampilkan semua kategori"""
    kategori_list = Kategori.get_all_kategori()
    return render_template('read_kategori.html', kategori_list=kategori_list)

@app.route('/kategori/create', methods=['GET', 'POST'])
@admin_required
def create_kategori():
    """Membuat kategori baru (admin only)"""
    if request.method == 'POST':
        kode_kategori = request.form.get('kode_kategori', '').strip()
        nama_kategori = request.form.get('nama_kategori', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        lokasi_rak = request.form.get('lokasi_rak', '').strip()
        
        if not all([kode_kategori, nama_kategori, deskripsi, lokasi_rak]):
            flash('Semua field harus diisi.', 'warning')
            return render_template('create_kategori.html')
        
        try:
            Kategori.create_kategori(kode_kategori, nama_kategori, deskripsi, lokasi_rak)
            flash('Kategori berhasil ditambahkan!', 'success')
            return redirect(url_for('read_kategori'))
        except Exception as e:
            flash(f'Gagal menambahkan kategori: {str(e)}', 'danger')
    
    return render_template('create_kategori.html')

@app.route('/kategori/update/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_kategori(id):
    """Mengupdate kategori (admin only)"""
    kategori = Kategori.get_kategori_by_id(id)
    if not kategori:
        flash('Kategori tidak ditemukan.', 'danger')
        return redirect(url_for('read_kategori'))
    
    if request.method == 'POST':
        kode_kategori = request.form.get('kode_kategori', '').strip()
        nama_kategori = request.form.get('nama_kategori', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        lokasi_rak = request.form.get('lokasi_rak', '').strip()
        
        if not all([kode_kategori, nama_kategori, deskripsi, lokasi_rak]):
            flash('Semua field harus diisi.', 'warning')
            return render_template('update_kategori.html', kategori=kategori)
        
        try:
            Kategori.update_kategori(id, kode_kategori, nama_kategori, deskripsi, lokasi_rak)
            flash('Kategori berhasil diperbarui!', 'success')
            return redirect(url_for('read_kategori'))
        except Exception as e:
            flash(f'Gagal memperbarui kategori: {str(e)}', 'danger')
    
    return render_template('update_kategori.html', kategori=kategori)

@app.route('/kategori/delete/<int:id>')
@admin_required
def delete_kategori(id):
    """Menghapus kategori beserta semua produk terkait (admin only)"""
    try:
        # Hapus kategori (produk terkait akan terhapus otomatis via ON DELETE CASCADE)
        Kategori.delete_kategori(id)
        flash('Kategori beserta produk terkait berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Gagal menghapus kategori: {str(e)}', 'danger')
    
    return redirect(url_for('read_kategori'))

# ============================================================
# CRUD PRODUK
# ============================================================

@app.route('/produk')
@login_required
def read_produk():
    """Menampilkan semua produk"""
    produk_list = Produk.get_all_produk()
    return render_template('read_produk.html', produk_list=produk_list)

@app.route('/produk/create', methods=['GET', 'POST'])
@admin_required
def create_produk():
    """Membuat produk baru (admin only)"""
    kategori_list = Kategori.get_all_kategori()
    
    if request.method == 'POST':
        kode_produk = request.form.get('kode_produk', '').strip()
        nama = request.form.get('nama', '').strip()
        harga = request.form.get('harga', '0')
        stok = request.form.get('stok', '0')
        kategori_id = request.form.get('kategori_id', '')
        
        if not all([kode_produk, nama, harga, kategori_id]):
            flash('Semua field harus diisi.', 'warning')
            return render_template('create_produk.html', kategori_list=kategori_list)
        
        try:
            Produk.create_produk(kode_produk, nama, int(harga), int(stok), int(kategori_id))
            flash('Produk berhasil ditambahkan!', 'success')
            return redirect(url_for('read_produk'))
        except Exception as e:
            flash(f'Gagal menambahkan produk: {str(e)}', 'danger')
    
    return render_template('create_produk.html', kategori_list=kategori_list)

@app.route('/produk/update/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_produk(id):
    """Mengupdate produk (admin only)"""
    produk = Produk.get_produk_by_id(id)
    kategori_list = Kategori.get_all_kategori()
    
    if not produk:
        flash('Produk tidak ditemukan.', 'danger')
        return redirect(url_for('read_produk'))
    
    if request.method == 'POST':
        kode_produk = request.form.get('kode_produk', '').strip()
        nama = request.form.get('nama', '').strip()
        harga = request.form.get('harga', '0')
        stok = request.form.get('stok', '0')
        kategori_id = request.form.get('kategori_id', '')
        
        if not all([kode_produk, nama, harga, kategori_id]):
            flash('Semua field harus diisi.', 'warning')
            return render_template('update_produk.html', produk=produk, kategori_list=kategori_list)
        
        try:
            Produk.update_produk(id, kode_produk, nama, int(harga), int(stok), int(kategori_id))
            flash('Produk berhasil diperbarui!', 'success')
            return redirect(url_for('read_produk'))
        except Exception as e:
            flash(f'Gagal memperbarui produk: {str(e)}', 'danger')
    
    return render_template('update_produk.html', produk=produk, kategori_list=kategori_list)

@app.route('/produk/delete/<int:id>')
@admin_required
def delete_produk(id):
    """Menghapus produk (admin only)"""
    try:
        Produk.delete_produk(id)
        flash('Produk berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Gagal menghapus produk: {str(e)}', 'danger')
    
    return redirect(url_for('read_produk'))

# ============================================================
# CRUD USER (Admin Only)
# ============================================================

@app.route('/user')
@admin_required
def read_user():
    """Menampilkan semua user (admin only)"""
    user_list = User.get_all_users()
    return render_template('read_user.html', user_list=user_list)

@app.route('/user/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Membuat user baru (admin only)"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'kasir')
        
        if not all([username, password]):
            flash('Semua field harus diisi.', 'warning')
            return render_template('create_user.html')
        
        try:
            User.create_user(username, password, role)
            flash('User berhasil ditambahkan!', 'success')
            return redirect(url_for('read_user'))
        except Exception as e:
            flash(f'Gagal menambahkan user: {str(e)}', 'danger')
    
    return render_template('create_user.html')

@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
@admin_required
def update_user(id):
    """Mengupdate user (admin only)"""
    user = User.get_user_by_id(id)
    
    if not user:
        flash('User tidak ditemukan.', 'danger')
        return redirect(url_for('read_user'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'kasir')
        
        if not username:
            flash('Username harus diisi.', 'warning')
            return render_template('update_user.html', user=user)
        
        try:
            User.update_user(id, username, role, password if password else None)
            flash('User berhasil diperbarui!', 'success')
            return redirect(url_for('read_user'))
        except Exception as e:
            flash(f'Gagal memperbarui user: {str(e)}', 'danger')
    
    return render_template('update_user.html', user=user)

@app.route('/user/delete/<int:id>')
@admin_required
def delete_user(id):
    """Menghapus user (admin only)"""
    # Cegah menghapus diri sendiri
    if id == session.get('user_id'):
        flash('Anda tidak dapat menghapus akun Anda sendiri.', 'warning')
        return redirect(url_for('read_user'))
    
    try:
        User.delete_user(id)
        flash('User berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Gagal menghapus user: {str(e)}', 'danger')
    
    return redirect(url_for('read_user'))

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(e):
    """Handler untuk halaman tidak ditemukan - tanpa flash message"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handler untuk error server"""
    return render_template('index.html'), 500

# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)
