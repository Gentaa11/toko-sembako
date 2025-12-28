"""
==============================================
Flask Application - Toko Sembako Murah Jaya
==============================================
"""

import os
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from models import User, Produk, Kategori
from pymysql import err as pymysql_err

logger = logging.getLogger(__name__)

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
app.secret_key = os.getenv('SECRET_KEY', 'toko_sembako_secret_key_2025_change_in_production')
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ============================================================
# DECORATOR
# ============================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
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
# CONTEXT PROCESSOR
# ============================================================

@app.context_processor
def inject_user():
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
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        produk_list = Produk.get_all_produk()
        kategori_list = Kategori.get_all_kategori()
        user_list = User.get_all_users() if session.get('role') == 'admin' else []
        
        # Ambil 5 produk terbaru (ID terbesar = paling baru ditambahkan)
        produk_terbaru = Produk.get_produk_terbaru(5)

        stats = {
            'total_produk': len(produk_list) if produk_list else 0,
            'total_kategori': len(kategori_list) if kategori_list else 0,
            'total_user': len(user_list) if user_list else 0,
            'total_stok': sum([p['stok'] for p in produk_list]) if produk_list else 0
        }
        return render_template('dashboard.html', stats=stats, produk_terbaru=produk_terbaru if produk_terbaru else [])
    except Exception as e:
        logger.exception('DB error saat mengambil data dashboard')
        flash('Terjadi kesalahan saat memuat dashboard.', 'danger')
        return render_template('dashboard.html', stats={'total_produk': 0, 'total_kategori': 0, 'total_user': 0, 'total_stok': 0}, produk_terbaru=[])

# ============================================================
# AUTENTIKASI
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember')

        if not username or not password:
            flash('Username dan password harus diisi.', 'warning')
            return render_template('login.html')

        try:
            user = User.check_login(username, password)
        except Exception as e:
            logger.exception('DB error saat login')
            flash('Terjadi kesalahan server. Silakan coba lagi nanti.', 'danger')
            return render_template('login.html')

        if user:
            session['user_id'] = user['id_user']
            session['username'] = user['username']
            session['role'] = user['role']
            if remember:
                session.permanent = True
            flash(f'Log in berhasil, Selamat datang {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user dan hapus session"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Sampai jumpa, {username}! Anda telah berhasil logout.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password:
            flash('Semua field harus diisi.', 'warning')
            return render_template('register.html')

        if len(password) < 4:
            flash('Password minimal 4 karakter.', 'warning')
            return render_template('register.html')

        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'danger')
            return render_template('register.html')

        try:
            User.create_user(username, password, 'kasir')
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
        except pymysql_err.IntegrityError:
            flash('Username sudah digunakan. Silakan pilih username lain.', 'danger')
        except Exception as e:
            logger.exception('Error saat registrasi user')
            flash('Terjadi kesalahan saat membuat user. Silakan coba lagi nanti.', 'danger')

    return render_template('register.html')

# ============================================================
# CRUD KATEGORI
# ============================================================

@app.route('/kategori')
@login_required
def read_kategori():
    try:
        kategori_list = Kategori.get_all_kategori()
    except Exception:
        logger.exception('DB error saat mengambil kategori')
        flash('Gagal memuat data kategori.', 'danger')
        kategori_list = []
    return render_template('read_kategori.html', kategori_list=kategori_list)

@app.route('/kategori/create', methods=['GET', 'POST'])
@admin_required
def create_kategori():
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
    try:
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
    try:
        produk_list = Produk.get_all_produk()
    except Exception:
        logger.exception('DB error saat mengambil produk')
        flash('Gagal memuat data produk.', 'danger')
        produk_list = []
    return render_template('read_produk.html', produk_list=produk_list)

@app.route('/produk/create', methods=['GET', 'POST'])
@admin_required
def create_produk():
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
    try:
        Produk.delete_produk(id)
        flash('Produk berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Gagal menghapus produk: {str(e)}', 'danger')
    return redirect(url_for('read_produk'))

# ============================================================
# CRUD USER
# ============================================================

@app.route('/user')
@admin_required
def read_user():
    try:
        user_list = User.get_all_users()
    except Exception:
        logger.exception('DB error saat mengambil user')
        flash('Gagal memuat data user.', 'danger')
        user_list = []
    return render_template('read_user.html', user_list=user_list)

@app.route('/user/create', methods=['GET', 'POST'])
@admin_required
def create_user():
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
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.exception('Unhandled server error')
    return render_template('index.html', error='Terjadi kesalahan server.'), 500

# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)