-- ================================================================
-- DATABASE: toko_sembako
-- SISTEM INFORMASI TOKO SEMBAKO MURAH JAYA
-- ================================================================
-- 
-- Deskripsi  : Database untuk sistem manajemen toko sembako
-- Versi      : 1.0.0
-- Tanggal    : Desember 2025
-- Author     : Next-Gen Tech
-- 
-- ================================================================

-- ================================================================
-- SETUP DATABASE
-- ================================================================

CREATE DATABASE IF NOT EXISTS toko_sembako
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE toko_sembako;

-- ================================================================
-- TABEL: kategori
-- ================================================================

DROP TABLE IF EXISTS produk;
DROP TABLE IF EXISTS kategori;
DROP TABLE IF EXISTS users;

CREATE TABLE kategori (
    id_kategori INT(11) NOT NULL AUTO_INCREMENT,
    kode_kategori VARCHAR(50) NOT NULL,
    nama_kategori VARCHAR(50) NOT NULL,
    deskripsi TEXT NOT NULL,
    lokasi_rak VARCHAR(25) NOT NULL,
    PRIMARY KEY (id_kategori),
    UNIQUE KEY uk_kode_kategori (kode_kategori),
    INDEX idx_nama_kategori (nama_kategori)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- TABEL: produk
-- ================================================================

CREATE TABLE produk (
    id_produk INT(11) NOT NULL AUTO_INCREMENT,
    kode_produk VARCHAR(20) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    harga INT(11) NOT NULL,
    stok INT(11) NOT NULL DEFAULT 0,
    kategori_id INT(11) NOT NULL,
    PRIMARY KEY (id_produk),
    INDEX idx_kode_produk (kode_produk),
    INDEX idx_nama_produk (nama),
    INDEX idx_kategori (kategori_id),
    CONSTRAINT fk_produk_kategori 
        FOREIGN KEY (kategori_id) REFERENCES kategori(id_kategori)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- TABEL: users
-- ================================================================

CREATE TABLE users (
    id_user INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    role VARCHAR(25) NOT NULL DEFAULT 'kasir',
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_user),
    UNIQUE KEY uk_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- DATA: kategori (35 records)
-- ================================================================

INSERT INTO kategori (id_kategori, kode_kategori, nama_kategori, deskripsi, lokasi_rak) VALUES
(1, 'KAT-001', 'Beras', 'Berbagai jenis beras (premium, medium, merah)', 'Area Lantai 1'),
(2, 'KAT-002', 'Minyak Goreng', 'Minyak goreng kelapa sawit kemasan bantal dan botol', 'Rak A1'),
(3, 'KAT-003', 'Gula Pasir', 'Gula pasir putih, gula merah, dan gula batu', 'Rak A2'),
(4, 'KAT-004', 'Tepung Terigu', 'Tepung terigu protein tinggi, sedang, dan rendah', 'Rak A3'),
(5, 'KAT-005', 'Telur', 'Telur ayam ras, telur bebek, dan telur puyuh', 'Rak Telur'),
(6, 'KAT-006', 'Mie Instan Goreng', 'Aneka merek mie instan varian goreng', 'Rak B1'),
(7, 'KAT-007', 'Mie Instan Kuah', 'Aneka merek mie instan varian kuah (soto, ayam, dll)', 'Rak B2'),
(8, 'KAT-008', 'Bihun & Sohun', 'Bihun jagung, bihun beras, dan sohun', 'Rak B3'),
(9, 'KAT-009', 'Pasta & Spaghetti', 'Spaghetti la fonte, macaroni, dan jenis pasta lainnya', 'Rak B3'),
(10, 'KAT-010', 'Makanan Kaleng', 'Sarden, kornet sapi, dan buah kaleng', 'Rak B4'),
(11, 'KAT-011', 'Kopi Bubuk', 'Kopi hitam bubuk berbagai merek lokal', 'Rak C1'),
(12, 'KAT-012', 'Kopi Instan Sachet', 'Kopi mix, cappuccino, dan kopi susu sachet', 'Rak C2'),
(13, 'KAT-013', 'Teh', 'Teh celup, teh tubruk, dan teh hijau', 'Rak C3'),
(14, 'KAT-014', 'Susu Kental Manis', 'SKM putih dan cokelat kaleng atau sachet', 'Rak C4'),
(15, 'KAT-015', 'Susu Bubuk & UHT', 'Susu bubuk keluarga, susu bayi, dan susu cair kotak', 'Rak C5'),
(16, 'KAT-016', 'Air Mineral', 'Air mineral galon, botol, dan gelas', 'Area Depan'),
(17, 'KAT-017', 'Minuman Ringan', 'Soft drink, teh kemasan botol, dan minuman berasa', 'Kulkas 1'),
(18, 'KAT-018', 'Sirup & Madu', 'Sirup aneka rasa dan madu murni', 'Rak C6'),
(19, 'KAT-019', 'Kecap', 'Kecap manis dan kecap asin berbagai ukuran', 'Rak D1'),
(20, 'KAT-020', 'Saus Sambal & Tomat', 'Saus sambal pedas dan saus tomat botol/pouch', 'Rak D2'),
(21, 'KAT-021', 'Garam & Penyedap', 'Garam meja, micin, kaldu bubuk, dan terasi', 'Rak D3'),
(22, 'KAT-022', 'Bumbu Instan', 'Bumbu racik nasi goreng, sayur asem, rendang, dll', 'Rak D4'),
(23, 'KAT-023', 'Santan Kemasan', 'Santan instan cair dan bubuk', 'Rak D4'),
(24, 'KAT-024', 'Mentega & Margarin', 'Margarin sachet dan kiloan untuk memasak/roti', 'Rak D5'),
(25, 'KAT-025', 'Deterjen Pakaian', 'Deterjen bubuk dan cair untuk mencuci baju', 'Rak E1'),
(26, 'KAT-026', 'Pewangi Pakaian', 'Pewangi dan pelembut pakaian sachet/pouch', 'Rak E2'),
(27, 'KAT-027', 'Sabun Cuci Piring', 'Sabun cuci piring cair dan krim', 'Rak E3'),
(28, 'KAT-028', 'Pembersih Lantai', 'Cairan pel lantai dan pembersih kamar mandi', 'Rak E4'),
(29, 'KAT-029', 'Sabun Mandi', 'Sabun mandi batang dan cair (body wash)', 'Rak F1'),
(30, 'KAT-030', 'Sampo & Kondisioner', 'Sampo sachet dan botol berbagai varian', 'Rak F2'),
(31, 'KAT-031', 'Pasta & Sikat Gigi', 'Pasta gigi berbagai ukuran dan sikat gigi', 'Rak F3'),
(32, 'KAT-032', 'Pembalut & Popok', 'Pembalut wanita dan popok bayi/dewasa', 'Rak F4'),
(33, 'KAT-033', 'Obat Nyamuk', 'Obat nyamuk bakar, semprot, dan elektrik', 'Rak G1'),
(34, 'KAT-034', 'Tisu', 'Tisu wajah, tisu toilet, dan kapas', 'Rak G2'),
(35, 'KAT-035', 'Gas & Galon', 'Gas LPG 3kg/12kg dan Galon air isi ulang', 'Gudang Belakang');

-- ================================================================
-- DATA: produk (35 records)
-- ================================================================

INSERT INTO produk (id_produk, kode_produk, nama, harga, stok, kategori_id) VALUES
(1, 'BRS-001', 'Beras Raja Lele (Karung 5kg)', 72000, 26, 1),
(2, 'BRS-002', 'Beras Pandan Wangi (Karung 10kg)', 145000, 10, 1),
(3, 'BRS-003', 'Beras IR 64 Premium (Eceran/Liter)', 13500, 48, 1),
(4, 'MNY-001', 'Minyak Goreng Bimoli Klasik Pouch 1L', 21000, 48, 2),
(5, 'MNY-002', 'Minyak Goreng Sunco Pouch 2L', 41500, 24, 2),
(6, 'MNY-003', 'Minyak Goreng Curah Plastik 1L', 16500, 50, 2),
(7, 'MNY-004', 'Minyak Goreng Filma Pouch 2L', 40000, 20, 2),
(8, 'GLP-001', 'Gula Pasir Gulaku Kuning 1kg', 17500, 50, 3),
(9, 'GLP-002', 'Gula Pasir Gulaku Premium Putih 1kg', 18000, 40, 3),
(10, 'GLP-003', 'Gula Pasir Curah (Putih) 1kg', 16000, 100, 3),
(11, 'GLP-004', 'Gula Merah Batok (per pcs)', 3500, 50, 3),
(12, 'TLR-001', 'Telur Ayam Negeri (per kg)', 29000, 30, 5),
(13, 'TLR-002', 'Telur Puyuh (per pack mika)', 10000, 15, 5),
(14, 'TLR-003', 'Telur Bebek Asin Matang (per butir)', 4000, 50, 5),
(15, 'MIE-001', 'Indomie Goreng Original 85g', 3100, 200, 6),
(16, 'MIE-002', 'Indomie Goreng Rendang 90g', 3100, 100, 6),
(17, 'MIE-003', 'Mie Sedaap Goreng Asli 90g', 3000, 150, 6),
(18, 'MIE-004', 'Indomie Goreng Jumbo 120g', 4500, 40, 6),
(19, 'KOP-001', 'Kapal Api Special Mix (Renceng 10x24g)', 15000, 50, 11),
(20, 'KOP-002', 'Kapal Api Special Bubuk 65g', 5500, 40, 11),
(21, 'KOP-003', 'Luwak White Coffee Original (Renceng 10s)', 14500, 30, 11),
(22, 'KOP-004', 'Top Coffee Gula Aren (Renceng 10s)', 11000, 25, 11),
(23, 'KOP-005', 'Indocafe Coffeemix (Pack 30s)', 48000, 15, 11),
(24, 'SPC-001', 'Sunlight Jeruk Nipis Pouch 755ml', 18500, 24, 27),
(25, 'SPC-002', 'Sunlight Jeruk Nipis Pouch Kecil 210ml', 5000, 48, 27),
(26, 'SPC-003', 'Mama Lemon Ekstrak Lemon Pouch 780ml', 16000, 20, 27),
(27, 'SPC-004', 'Ekonomi Sabun Colek Cream 145g', 2500, 60, 27),
(28, 'TPG-001', 'Tepung Segitiga Biru 1kg', 14500, 30, 4),
(29, 'TPG-002', 'Tepung Cakra Kembar (Protein Tinggi) 1kg', 16000, 20, 4),
(30, 'TEH-001', 'Teh Sariwangi Asli (Box 25s)', 6500, 40, 13),
(31, 'TEH-002', 'Teh Tubruk Cap Botol (Bungkus Kertas)', 3500, 60, 13),
(32, 'KCP-001', 'Kecap Bango Manis Pouch 520ml', 24500, 24, 19),
(33, 'KCP-002', 'Kecap Sedaap Manis Pouch 520ml', 19500, 24, 19),
(34, 'DET-001', 'Rinso Anti Noda Deterjen Bubuk 770g', 26500, 20, 25),
(35, 'DET-002', 'Daia Deterjen Bunga 850g', 18000, 26, 25);

-- ================================================================
-- USERS: Dibuat via aplikasi
-- ================================================================
-- 
-- CATATAN: Data users TIDAK disertakan untuk keamanan.
-- 
-- Cara membuat user:
--   1. Jalankan aplikasi: python app.py
--   2. Akses halaman: http://127.0.0.1:5000/register
--   3. Daftar user baru dengan role yang diinginkan
-- 
-- Atau gunakan pass.py untuk generate hash:
--   python pass.py
-- 
-- ================================================================

-- Verifikasi data
SELECT 'kategori' AS tabel, COUNT(*) AS jumlah FROM kategori
UNION ALL
SELECT 'produk' AS tabel, COUNT(*) AS jumlah FROM produk
UNION ALL
SELECT 'users' AS tabel, COUNT(*) AS jumlah FROM users;

-- ================================================================
-- END OF FILE
-- ================================================================