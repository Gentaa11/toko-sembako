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
-- Tabel      : 
--   1. kategori - Kategori produk sembako
--   2. produk   - Data produk dengan relasi ke kategori
--   3. users    - Data pengguna dengan role admin/kasir
-- 
-- Relasi     : produk.kategori_id → kategori.id_kategori
--              ON DELETE CASCADE, ON UPDATE CASCADE
-- 
-- Cara Import:
--   Via phpMyAdmin : Import → Pilih file ini → Go
--   Via CLI        : mysql -u root -p < toko_sembako.sql
-- 
-- ================================================================

-- ================================================================
-- SETUP DATABASE
-- ================================================================

-- Hapus database jika ada (HATI-HATI di production!)
-- DROP DATABASE IF EXISTS toko_sembako;

-- Buat database
CREATE DATABASE IF NOT EXISTS toko_sembako
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Gunakan database
USE toko_sembako;

-- ================================================================
-- TABEL: kategori
-- Menyimpan kategori/jenis produk sembako
-- ================================================================

DROP TABLE IF EXISTS produk;  -- Drop child table first (foreign key)
DROP TABLE IF EXISTS kategori;

CREATE TABLE kategori (
    id_kategori INT(11) NOT NULL AUTO_INCREMENT,
    kode_kategori VARCHAR(50) NOT NULL,
    nama_kategori VARCHAR(50) NOT NULL,
    deskripsi TEXT NOT NULL,
    lokasi_rak VARCHAR(25) NOT NULL,
    
    -- Constraints
    PRIMARY KEY (id_kategori),
    UNIQUE KEY uk_kode_kategori (kode_kategori),
    
    -- Index untuk pencarian
    INDEX idx_nama_kategori (nama_kategori)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Tabel kategori produk sembako';

-- ================================================================
-- TABEL: produk
-- Menyimpan data produk dengan relasi ke kategori
-- ================================================================

DROP TABLE IF EXISTS produk;

CREATE TABLE produk (
    id_produk INT(11) NOT NULL AUTO_INCREMENT,
    kode_produk VARCHAR(20) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    harga INT(11) NOT NULL,
    stok INT(11) NOT NULL DEFAULT 0,
    kategori_id INT(11) NOT NULL,
    
    -- Constraints
    PRIMARY KEY (id_produk),
    
    -- Index untuk pencarian dan filter
    INDEX idx_kode_produk (kode_produk),
    INDEX idx_nama_produk (nama),
    INDEX idx_kategori (kategori_id),
    INDEX idx_stok (stok),
    
    -- Foreign Key dengan CASCADE
    CONSTRAINT fk_produk_kategori 
        FOREIGN KEY (kategori_id) REFERENCES kategori(id_kategori)
        ON DELETE CASCADE
        ON UPDATE CASCADE
        
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Tabel produk sembako';

-- ================================================================
-- TABEL: users
-- Menyimpan data pengguna sistem (admin/kasir)
-- ================================================================

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id_user INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    role VARCHAR(25) NOT NULL DEFAULT 'kasir',
    password VARCHAR(255) NOT NULL,
    
    -- Constraints
    PRIMARY KEY (id_user),
    UNIQUE KEY uk_username (username),
    
    -- Index untuk login
    INDEX idx_role (role)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Tabel pengguna sistem';

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
-- DATA: users (35 records)
-- Password: "password123" untuk semua user
-- Hash menggunakan Werkzeug Scrypt
-- ================================================================

INSERT INTO users (id_user, username, role, password) VALUES
(1, 'Genta', 'admin', 'scrypt:32768:8:1$SOEJsNHavRkXuCbp$3d349c8f9aa2fe479319ee12318a7dd5f88cdb943d8901f3bcbac01c06267397eca41922995eebd29034415c075df0c779dcb5704b1e037555e5d23cf962ec56'),
(2, 'Budi Santoso', 'admin', 'scrypt:32768:8:1$1QU63XWH6zpeypL1$0505248a3b10b4051d7354cc4260a7371965a6691738b4009aaab062cd55066cfe8457a48fd200a53bf46bcc734cc23a5d260dad4a1083232874efc0e2592047'),
(3, 'Siti Aminah', 'admin', 'scrypt:32768:8:1$W6AMb8XV7ttMLSKR$da8c1546cc32bca202e2abda5cafceac9aee9f68e29853778a3ac177690a3dd9032dd66dd6be2c10054c33991e28aeeedfe1a315b85cd005701528fe93fa421b'),
(4, 'Reza Pratama', 'admin', 'scrypt:32768:8:1$WXnPZqlpjS8IDu9z$60fcb3b264a7dbbafc7f7369a9ebd577f4a27353c267752770ad476747889b1c29785f3e91a6fc7575dd9efd9c5c77354fc9c59e57231af5fd5614557ef71549'),
(5, 'Dewi Sartika', 'admin', 'scrypt:32768:8:1$WbxbsgeA502EfXFy$c1940ca62fffbb525388a1c84318f19605553d9bf56c947fed12c92d5dbde8e8de52c100387167dcb341f9f3dccebc1b441d80dceae57725f4eff901743bb2fa'),
(6, 'Andi Wijaya', 'admin', 'scrypt:32768:8:1$kxZxl9Gpx1QOTNwp$c6fd143b70d1d31b1ac6eeb94a695ae4965ae01748cd763dab303c3c19df6234bdf18d0d2eab42b34894f31a81abad520a3543a6ed42200722f68f1337052e5d'),
(7, 'Rina Hartati', 'admin', 'scrypt:32768:8:1$iSSbfa2VXPqMgkdV$7dedf64ebda9986a25113963d686414e6cd795c08316b9be87e0d6f92fb0900f9b6aa1f25a436a21b78874653a6aeb8c06e00d2db2c6e09c60d757fe90410729'),
(8, 'Eko Saputra', 'admin', 'scrypt:32768:8:1$352uaFSLLc5YdFai$5ef2322d502edd9cce7e0c4bc16cc5614bf20f64761671d99056284ef198227a2253af8fdebfd394b523b73e6d26828e3730c1d81219580e9d6941844b74d81f'),
(9, 'Sari Indah', 'admin', 'scrypt:32768:8:1$JBpptyb4yMhDwsCo$845f60c8d9668140a64210768063b4001ec29f34459d34dcb1639a7c911193604cd76f9c7517853d0216e77ba5fcc048853463f531daaa148daca0464b17b854'),
(10, 'Agus Setiawan', 'admin', 'scrypt:32768:8:1$JHedrv5lzOZmjbFq$5a0bf481482f3a9f3d10819fc8fbf6f2b452f2938880507f1b30a4607deaa3512a41cc7e99308fb95e6b335e8316ca5fc5c8806e7d39f192d9f2cb278be5b631'),
(11, 'Tono Sudiro', 'kasir', 'scrypt:32768:8:1$eNgz5U985KX9ICl0$b33c4e75064edc207a054182d1c2286a9818b0da4550fe5450710ddd3ac054af8bb49ef0330490e39c909fa685ae58c3061f8eb61a67f93c61b22cfd7efbd094'),
(12, 'Yanti Putri', 'kasir', 'scrypt:32768:8:1$0fHTmhLQqJIYMnHX$fd2d14d397b34818bd355f3375c21ad7b8c3d503d77722d66b457c0db6dedbe628bdd905e1b7a1919b0678f95916130446074b232b15a5a8d8afd00be2f0aaf6'),
(13, 'Joko Anwar', 'kasir', 'scrypt:32768:8:1$i15aoWjGKR12SSje$e55abef9b5dcc877d319cbb07de511ada73268639f8de6ebfb564700ce6dd6feef320953c7cb3149beff267a5dbfd69ebf4789b9d1e4b65480c35317df479555'),
(14, 'Sri Wahyuni', 'kasir', 'scrypt:32768:8:1$NmBxjjKK6n6lJ4DC$40f12d4cc8a28fc9f391f72626ce9a5128004c03347892ac80014470b62203f780c06a1c226575e091aaf1066622244f7aa8ec10d3ba0b1c897f37e349d6ecfa'),
(15, 'Dian Permata', 'kasir', 'scrypt:32768:8:1$06n5FsaCOiGXgjVy$58d199d25188204e155f761d084bf43283617f8f1b39b884ae27e69d7fcce1af43364d194694b8c8d07d4a33e233c67dc08f36bceabd4e19a5d8c575b0008f96'),
(16, 'Bayu Nugraha', 'kasir', 'scrypt:32768:8:1$OrXSsjuWzVt4vw0N$15a9f87d28c2b6b71d14fd094c80f20ac8734b03e4fd63ec0cf42517028ff77a7e03c75c6ff99d9091f61c94feee4b1931885cc6c6bce1f6dfa96d8a47acc8ad'),
(17, 'Tari Lestari', 'kasir', 'scrypt:32768:8:1$3qWhVXFs5M7KzyNz$4f72377226d937e7a7295aa8b2678ac21683af413b277ab10b09e4b3025b5af98ebb03ee42f9f5bf98a6616442205ce93dbda87e428db2159c3371443352eb96'),
(18, 'Rizky Fajar', 'kasir', 'scrypt:32768:8:1$epUE3ccEaLOHawah$df6cef4dda547d3b52adf510524aa0e5a7dd780f9442ac0d1f8fd7094c537a2217cad2ece5ced03038778f8e5af7843a955e4ce21e818b28e579d71e5ceec435'),
(19, 'Nur Hidayah', 'kasir', 'scrypt:32768:8:1$8MmkW1ycjsv8g1iu$a54015a96caddd54b73904f1f521d86ef53bb27ba2d100b6955f0852304a06cb6e69c49bc1ba7805e41dc23c9ea35ff6bb9e265d57aa4209f4970937ca9299ac'),
(20, 'Ilham Ramadhan', 'kasir', 'scrypt:32768:8:1$Vzl2d6tJlwPXcTX9$af09da24e49deef42ea4b87a33352af22d4fe5de160d68f8917b06878aaa147d90d57171da49e095cb97595d6bb46623285ad0908c08185a3e91279cc5d52581'),
(21, 'Mega Puspa', 'kasir', 'scrypt:32768:8:1$BfLfEmeogYunV05M$7c35c461c39d6794c49e790dd28713c9aa83de8112ebf6fba2b03f993dcd1a6f480d7240f61800477c6dc1f88c47dd247071def4281bf589954f3ba06c14159a'),
(22, 'Fajar Sidik', 'kasir', 'scrypt:32768:8:1$MiSuQHOTKaI7oxFa$3e142f88b9dd535b83d59589f55c1d912443892f6bb2fdb97a5ac958c37fee756528ad56802a74cf0e63d813a328951612d7d588d1a68e6fb9b2348451f35975'),
(23, 'Indah Cahaya', 'kasir', 'scrypt:32768:8:1$lWOSjTpaNFQZzoDy$1ba2de92328205a56a154b2bcd8cc615dda94a3eddcfb202ac1d9f4f2cb873b34a1cc857574f6b5ab4372dbee4c8f36fbc2c8908f318ef5f2e6c9d4f2d18bfc3'),
(24, 'Dani Setiawan', 'kasir', 'scrypt:32768:8:1$79g477oPzihsvmnp$ce3be94ac413596aa57aa64699e3f0d7cb65ab1e834e485066781244bd3d7f54840f2198e52e011798f3ca0a2d872c07b209f52b20ec8180c44dbfe9201dd2fb'),
(25, 'Susi Susanti', 'kasir', 'scrypt:32768:8:1$KCm0PF7DY2VT27ky$9ca0e46d8ba81fb33609ad8e5afb7a2fa0b5b22397c63827c484186418f5531d106f7f56b85471ce01640b5f9c505447a5631ed7a2dff244e55e01833e7781ae'),
(26, 'Putra Bangsa', 'kasir', 'scrypt:32768:8:1$bS8m6MPnyTjzAyaI$53061b85bed85d6e6141863944a89c2cab6da143f248d4f0398f53313aa98f87545b2d6ae9cee15588e1d4668852eda5c7af794ccd450ea0d26a0cd2a4a98dae'),
(27, 'Lia Marlina', 'kasir', 'scrypt:32768:8:1$BB7WzRTAGGfuN8En$922b28c37b0c505ed6590affd6bf919557905dc91875ae86992955a06e8a0fa97cd553930045c84812941c29a71eb912ee1bc2e4074002dae4e3479582f26aa6'),
(28, 'Rendy Pangestu', 'kasir', 'scrypt:32768:8:1$E93VQOUY3IfB9B6D$d53b724bfb00f8648745169c852f14e72be0fdac8a898f8f3409b053eceab88e8b03b083fb36f56ad9744117f073fa127b44869243768b73f30cc2a7afb132f2'),
(29, 'Wulan Guritno', 'kasir', 'scrypt:32768:8:1$PFd0mq24KB8w2fkt$9126c4ae40565205d7df14542a4deec268ace5a8b588f5d92dec2af8cea25db06eff7ac4faad121d10cf6640a5705222d6a0d4919a49014bf921ef37a31d4f38'),
(30, 'Bambang Pamungkas', 'kasir', 'scrypt:32768:8:1$xQ41Pp7HodoNYGFx$256a810eb6e9707a4df7b738d9354d934d937507d7a6cd4bf659320f5f410b6aa4e091b532f63c43f6eb31c270df41755cae96ac8cd30c206ac9088f47f54107'),
(31, 'Rina Nose', 'kasir', 'scrypt:32768:8:1$225tqaDGspOhrNXg$68ef8db6ab3f330f38c787f6c633f2e35094f763353445fd8afcd2cb2f07ec0b1ceec413c00b58d94118f4603264fd75fdb58af78dd733c6e0ce97de5294674a'),
(32, 'Gilang Dirga', 'kasir', 'scrypt:32768:8:1$NrYp8Ll79nIE47Wv$79c3a351d29c86ee6c09acc713a368ff9951547dfbd01d0d0c8e5294e2e27ddb8688eed496553aa96c88fc460df08f9457d97e096678ea7bf92e28787dd93f15'),
(33, 'Ayu Tingting', 'kasir', 'scrypt:32768:8:1$Dxbyh6se3hiHzyh4$d0c772add920f5df1947cc097f96fa3a761614b6f0a6acdac392953642a5f2f83d9a7db9cc417242a03b23fa4b1ff89a857a0a348c3304c406c4e90cce03a91b'),
(34, 'Hendra Kusuma', 'kasir', 'scrypt:32768:8:1$SOEJsNHavRkXuCbp$3d349c8f9aa2fe479319ee12318a7dd5f88cdb943d8901f3bcbac01c06267397eca41922995eebd29034415c075df0c779dcb5704b1e037555e5d23cf962ec56'),
(35, 'Kartini Dewi', 'kasir', 'scrypt:32768:8:1$1QU63XWH6zpeypL1$0505248a3b10b4051d7354cc4260a7371965a6691738b4009aaab062cd55066cfe8457a48fd200a53bf46bcc734cc23a5d260dad4a1083232874efc0e2592047');

-- ================================================================
-- VERIFIKASI DATA
-- ================================================================

-- Tampilkan jumlah data per tabel
SELECT 'kategori' AS tabel, COUNT(*) AS jumlah FROM kategori
UNION ALL
SELECT 'produk' AS tabel, COUNT(*) AS jumlah FROM produk
UNION ALL
SELECT 'users' AS tabel, COUNT(*) AS jumlah FROM users;

-- ================================================================
-- CATATAN PENTING
-- ================================================================
-- 
-- 1. Password sudah di-hash menggunakan Werkzeug Scrypt
--    JANGAN mengubah nilai password secara manual
-- 
-- 2. Untuk menambah user baru, gunakan:
--    - Halaman /register di aplikasi, atau
--    - Python script dengan generate_password_hash()
-- 
-- 3. Relasi produk → kategori menggunakan CASCADE
--    Menghapus kategori akan menghapus semua produk terkait
-- 
-- 4. Backup database secara berkala:
--    mysqldump -u root -p toko_sembako > backup.sql
-- 
-- ================================================================
-- END OF FILE
-- ================================================================

