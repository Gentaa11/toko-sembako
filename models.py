
import os
import pymysql
import pymysql.err
from werkzeug.security import generate_password_hash, check_password_hash

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Database:

    def __init__(self):
        self.connection = None

    def _connect(self):
        if self.connection:
            try:
                self.connection.ping(reconnect=True)
                return
            except Exception:
                try:
                    self.connection.close()
                except Exception:
                    pass
                self.connection = None

        self.connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            db=os.getenv('DB_NAME', 'toko_sembako'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            connect_timeout=10
        )

    def execute(self, sql, params=None):
        cur = None
        try:
            self._connect()
            cur = self.connection.cursor()
            cur.execute(sql, params)
            self.connection.commit()
            return cur.rowcount
        except (pymysql.err.OperationalError, pymysql.err.InterfaceError):
            try:
                self._connect()
                if cur:
                    try:
                        cur.close()
                    except:
                        pass
                cur = self.connection.cursor()
                cur.execute(sql, params)
                self.connection.commit()
                return cur.rowcount
            except Exception:
                raise
        finally:
            if cur:
                try:
                    cur.close()
                except:
                    pass

    def fetchone(self, sql, params=None):
        cur = None
        try:
            self._connect()
            cur = self.connection.cursor()
            cur.execute(sql, params)
            return cur.fetchone()
        except (pymysql.err.OperationalError, pymysql.err.InterfaceError):
            try:
                self._connect()
                if cur:
                    try:
                        cur.close()
                    except:
                        pass
                cur = self.connection.cursor()
                cur.execute(sql, params)
                return cur.fetchone()
            except Exception:
                raise
        finally:
            if cur:
                try:
                    cur.close()
                except:
                    pass

    def fetchall(self, sql, params=None):
        cur = None
        try:
            self._connect()
            cur = self.connection.cursor()
            cur.execute(sql, params)
            return cur.fetchall()
        except (pymysql.err.OperationalError, pymysql.err.InterfaceError):
            try:
                self._connect()
                if cur:
                    try:
                        cur.close()
                    except:
                        pass
                cur = self.connection.cursor()
                cur.execute(sql, params)
                return cur.fetchall()
            except Exception:
                raise
        finally:
            if cur:
                try:
                    cur.close()
                except:
                    pass

    def close(self):
        try:
            if self.connection:
                self.connection.close()
        except:
            pass
        finally:
            self.connection = None


db = Database()


class User:

    @staticmethod
    def create_user(username, password, role='kasir'):
        hashed_password = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        db.execute(sql, (username, hashed_password, role))

    @staticmethod
    def check_login(username, password):
        sql = "SELECT * FROM users WHERE username = %s"
        user = db.fetchone(sql, (username,))
        if user and check_password_hash(user["password"], password):
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        sql = "SELECT * FROM users WHERE id_user = %s"
        return db.fetchone(sql, (user_id,))

    @staticmethod
    def get_all_users():
        sql = "SELECT id_user, username, role FROM users ORDER BY id_user"
        return db.fetchall(sql)

    @staticmethod
    def delete_user(user_id):
        sql = "DELETE FROM users WHERE id_user = %s"
        db.execute(sql, (user_id,))

    @staticmethod
    def update_user(user_id, username, role, password=None):
        if password:
            hashed_password = generate_password_hash(password)
            sql = "UPDATE users SET username = %s, password = %s, role = %s WHERE id_user = %s"
            db.execute(sql, (username, hashed_password, role, user_id))
        else:
            sql = "UPDATE users SET username = %s, role = %s WHERE id_user = %s"
            db.execute(sql, (username, role, user_id))


class Produk:

    @staticmethod
    def create_produk(kode_produk, nama, harga, stok, kategori_id):
        sql = """INSERT INTO produk (kode_produk, nama, harga, stok, kategori_id)
                 VALUES (%s, %s, %s, %s, %s)"""
        db.execute(sql, (kode_produk, nama, harga, stok, kategori_id))

    @staticmethod
    def get_produk_by_id(id_produk):
        sql = """SELECT p.id_produk, p.kode_produk, p.nama, p.harga, p.stok, p.kategori_id,
                        k.nama_kategori, k.lokasi_rak
                 FROM produk p
                 LEFT JOIN kategori k ON p.kategori_id = k.id_kategori
                 WHERE p.id_produk = %s"""
        return db.fetchone(sql, (id_produk,))

    @staticmethod
    def get_all_produk():
        sql = """SELECT p.id_produk, p.kode_produk, p.nama, p.harga, p.stok, p.kategori_id,
                        k.nama_kategori, k.lokasi_rak
                 FROM produk p
                 LEFT JOIN kategori k ON p.kategori_id = k.id_kategori
                 ORDER BY p.id_produk"""
        return db.fetchall(sql)

    @staticmethod
    def get_produk_terbaru(limit=5):
        """Ambil produk terbaru berdasarkan ID (terbesar = terbaru)."""
        sql = """SELECT p.id_produk, p.kode_produk, p.nama, p.harga, p.stok, p.kategori_id,
                        k.nama_kategori, k.lokasi_rak
                 FROM produk p
                 LEFT JOIN kategori k ON p.kategori_id = k.id_kategori
                 ORDER BY p.id_produk DESC
                 LIMIT %s"""
        return db.fetchall(sql, (limit,))

    @staticmethod
    def delete_produk(id_produk):
        sql = "DELETE FROM produk WHERE id_produk = %s"
        db.execute(sql, (id_produk,))

    @staticmethod
    def update_produk(id_produk, kode_produk, nama, harga, stok, kategori_id):
        sql = """UPDATE produk
                 SET kode_produk = %s, nama = %s, harga = %s, stok = %s, kategori_id = %s
                 WHERE id_produk = %s"""
        db.execute(sql, (kode_produk, nama, harga, stok, kategori_id, id_produk))

    @staticmethod
    def get_produk_by_kategori(kategori_id):
        sql = "SELECT * FROM produk WHERE kategori_id = %s ORDER BY nama"
        return db.fetchall(sql, (kategori_id,))


class Kategori:

    @staticmethod
    def create_kategori(kode_kategori, nama_kategori, deskripsi, lokasi_rak):
        sql = """INSERT INTO kategori (kode_kategori, nama_kategori, deskripsi, lokasi_rak)
                 VALUES (%s, %s, %s, %s)"""
        db.execute(sql, (kode_kategori, nama_kategori, deskripsi, lokasi_rak))

    @staticmethod
    def get_kategori_by_id(id_kategori):
        sql = "SELECT * FROM kategori WHERE id_kategori = %s"
        return db.fetchone(sql, (id_kategori,))

    @staticmethod
    def get_all_kategori():
        sql = "SELECT * FROM kategori ORDER BY id_kategori"
        return db.fetchall(sql)

    @staticmethod
    def delete_kategori(id_kategori):
        sql = "DELETE FROM kategori WHERE id_kategori = %s"
        db.execute(sql, (id_kategori,))

    @staticmethod
    def update_kategori(id_kategori, kode_kategori, nama_kategori, deskripsi, lokasi_rak):
        sql = """UPDATE kategori
                 SET kode_kategori = %s, nama_kategori = %s, deskripsi = %s, lokasi_rak = %s
                 WHERE id_kategori = %s"""
        db.execute(sql, (kode_kategori, nama_kategori, deskripsi, lokasi_rak, id_kategori))