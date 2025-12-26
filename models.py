"""
==============================================
Database Models - Toko Sembako Murah Jaya
==============================================

Module ini berisi semua operasi database untuk:
- Users (autentikasi & otorisasi)
- Produk (manajemen inventaris)
- Kategori (klasifikasi produk)

==============================================
"""

import os
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables (jika menggunakan python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv tidak terinstall, gunakan default values
    pass


class Database:
    """
    Database connection manager menggunakan PyMySQL.
    Mendukung konfigurasi via environment variables.
    """
    
    def __init__(self):
        """
        Inisialisasi koneksi database.
        Konfigurasi diambil dari environment variables atau default values.
        """
        self.connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            db=os.getenv('DB_NAME', 'toko_sembako'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    
    def query(self, sql, params=None):
        """Execute query dengan parameter."""
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.connection.commit()
        return cursor

    def fetchone(self, sql, params=None):
        """Execute query dan ambil satu hasil."""
        cursor = self.query(sql, params)
        return cursor.fetchone()

    def fetchall(self, sql, params=None):
        """Execute query dan ambil semua hasil."""
        cursor = self.query(sql, params)
        return cursor.fetchall()
    
    def close(self):
        """Tutup koneksi database."""
        if self.connection:
            self.connection.close()


# Global database instance
db = Database()


class User:
    """Model untuk operasi CRUD tabel users."""

    @staticmethod
    def create_user(username, password, role='kasir'):
        """
        Buat user baru dengan password yang di-hash.
        
        Args:
            username: Username unik
            password: Password plain text (akan di-hash)
            role: Role user ('admin' atau 'kasir')
        
        Raises:
            Exception: Jika username sudah ada
        """
        hashed_password = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        db.query(sql, (username, hashed_password, role))

    @staticmethod
    def check_login(username, password):
        """
        Verifikasi kredensial login.
        
        Args:
            username: Username
            password: Password plain text
        
        Returns:
            dict: Data user jika valid, None jika tidak valid
        """
        sql = "SELECT * FROM users WHERE username = %s"
        user = db.fetchone(sql, (username,))
        if user and check_password_hash(user["password"], password):
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        """Ambil user berdasarkan ID."""
        sql = "SELECT * FROM users WHERE id_user = %s"
        return db.fetchone(sql, (user_id,))

    @staticmethod
    def get_all_users():
        """Ambil semua user (tanpa password)."""
        sql = "SELECT id_user, username, role FROM users ORDER BY id_user"
        return db.fetchall(sql)

    @staticmethod
    def delete_user(user_id):
        """Hapus user berdasarkan ID."""
        sql = "DELETE FROM users WHERE id_user = %s"
        db.query(sql, (user_id,))

    @staticmethod
    def update_user(user_id, username, role, password=None):
        """
        Update data user.
        
        Args:
            user_id: ID user yang akan diupdate
            username: Username baru
            role: Role baru
            password: Password baru (opsional, jika None tidak diubah)
        """
        if password:
            hashed_password = generate_password_hash(password)
            sql = "UPDATE users SET username = %s, password = %s, role = %s WHERE id_user = %s"
            db.query(sql, (username, hashed_password, role, user_id))
        else:
            sql = "UPDATE users SET username = %s, role = %s WHERE id_user = %s"
            db.query(sql, (username, role, user_id))


class Produk:
    """Model untuk operasi CRUD tabel produk."""
    
    @staticmethod
    def create_produk(kode_produk, nama, harga, stok, kategori_id):
        """Buat produk baru."""
        sql = """INSERT INTO produk (kode_produk, nama, harga, stok, kategori_id) 
                 VALUES (%s, %s, %s, %s, %s)"""
        db.query(sql, (kode_produk, nama, harga, stok, kategori_id))

    @staticmethod
    def get_produk_by_id(id_produk):
        """Ambil produk berdasarkan ID dengan informasi kategori."""
        sql = """SELECT p.id_produk, p.kode_produk, p.nama, p.harga, p.stok, p.kategori_id,
                        k.nama_kategori, k.lokasi_rak
                 FROM produk p 
                 LEFT JOIN kategori k ON p.kategori_id = k.id_kategori 
                 WHERE p.id_produk = %s"""
        return db.fetchone(sql, (id_produk,))

    @staticmethod
    def get_all_produk():
        """Ambil semua produk dengan informasi kategori."""
        sql = """SELECT p.id_produk, p.kode_produk, p.nama, p.harga, p.stok, p.kategori_id,
                        k.nama_kategori, k.lokasi_rak
                 FROM produk p 
                 LEFT JOIN kategori k ON p.kategori_id = k.id_kategori
                 ORDER BY p.id_produk"""
        return db.fetchall(sql)

    @staticmethod
    def delete_produk(id_produk):
        """Hapus produk berdasarkan ID."""
        sql = "DELETE FROM produk WHERE id_produk = %s"
        db.query(sql, (id_produk,))

    @staticmethod
    def update_produk(id_produk, kode_produk, nama, harga, stok, kategori_id):
        """Update data produk."""
        sql = """UPDATE produk 
                 SET kode_produk = %s, nama = %s, harga = %s, stok = %s, kategori_id = %s 
                 WHERE id_produk = %s"""
        db.query(sql, (kode_produk, nama, harga, stok, kategori_id, id_produk))

    @staticmethod
    def get_produk_by_kategori(kategori_id):
        """Ambil semua produk dalam kategori tertentu."""
        sql = "SELECT * FROM produk WHERE kategori_id = %s ORDER BY nama"
        return db.fetchall(sql, (kategori_id,))


class Kategori:
    """Model untuk operasi CRUD tabel kategori."""
    
    @staticmethod
    def create_kategori(kode_kategori, nama_kategori, deskripsi, lokasi_rak):
        """Buat kategori baru."""
        sql = """INSERT INTO kategori (kode_kategori, nama_kategori, deskripsi, lokasi_rak) 
                 VALUES (%s, %s, %s, %s)"""
        db.query(sql, (kode_kategori, nama_kategori, deskripsi, lokasi_rak))

    @staticmethod
    def get_kategori_by_id(id_kategori):
        """Ambil kategori berdasarkan ID."""
        sql = "SELECT * FROM kategori WHERE id_kategori = %s"
        return db.fetchone(sql, (id_kategori,))

    @staticmethod
    def get_all_kategori():
        """Ambil semua kategori."""
        sql = "SELECT * FROM kategori ORDER BY id_kategori"
        return db.fetchall(sql)

    @staticmethod
    def delete_kategori(id_kategori):
        """
        Hapus kategori berdasarkan ID.
        Catatan: Produk terkait akan terhapus otomatis (ON DELETE CASCADE)
        """
        sql = "DELETE FROM kategori WHERE id_kategori = %s"
        db.query(sql, (id_kategori,))

    @staticmethod
    def update_kategori(id_kategori, kode_kategori, nama_kategori, deskripsi, lokasi_rak):
        """Update data kategori."""
        sql = """UPDATE kategori 
                 SET kode_kategori = %s, nama_kategori = %s, deskripsi = %s, lokasi_rak = %s 
                 WHERE id_kategori = %s"""
        db.query(sql, (kode_kategori, nama_kategori, deskripsi, lokasi_rak, id_kategori))
