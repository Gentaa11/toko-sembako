from werkzeug.security import generate_password_hash, check_password_hash


def generate_hash(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password: str, hash_value: str) -> bool:
    return check_password_hash(hash_value, password)


def main():
    print("=" * 50)
    print("  PASSWORD HASH GENERATOR")
    print("  Toko Sembako Murah Jaya")
    print("=" * 50)
    print()
    
    while True:
        print("Pilih opsi:")
        print("1. Generate hash dari password")
        print("2. Verifikasi password dengan hash")
        print("3. Generate user default (admin & kasir)")
        print("4. Keluar")
        print()
        
        choice = input("Pilihan (1-4): ").strip()
        print()
        
        if choice == "1":
            password = input("Masukkan password: ").strip()
            if password:
                hashed = generate_hash(password)
                print()
                print("Password Hash:")
                print("-" * 50)
                print(hashed)
                print("-" * 50)
                print()
                print("SQL untuk insert ke database:")
                print(f"INSERT INTO users (username, role, password) VALUES ('username', 'admin', '{hashed}');")
            else:
                print("Password tidak boleh kosong!")
            print()
            
        elif choice == "2":
            password = input("Masukkan password: ").strip()
            hash_value = input("Masukkan hash: ").strip()
            if password and hash_value:
                is_valid = verify_password(password, hash_value)
                print()
                if is_valid:
                    print("✅ Password COCOK dengan hash!")
                else:
                    print("❌ Password TIDAK COCOK dengan hash!")
            else:
                print("Password dan hash tidak boleh kosong!")
            print()
            
        elif choice == "3":
            print("Generating default users...")
            print()
            
            admin_pass = "admin123"
            admin_hash = generate_hash(admin_pass)
            print("👤 USER ADMIN")
            print(f"   Username: admin")
            print(f"   Password: {admin_pass}")
            print(f"   Role: admin")
            print()
            print("   SQL:")
            print(f"   INSERT INTO users (username, role, password) VALUES ('admin', 'admin', '{admin_hash}');")
            print()
            
            kasir_pass = "kasir123"
            kasir_hash = generate_hash(kasir_pass)
            print("👤 USER KASIR")
            print(f"   Username: kasir")
            print(f"   Password: {kasir_pass}")
            print(f"   Role: kasir")
            print()
            print("   SQL:")
            print(f"   INSERT INTO users (username, role, password) VALUES ('kasir', 'kasir', '{kasir_hash}');")
            print()
            
            print("-" * 50)
            print("Copy SQL di atas dan jalankan di phpMyAdmin atau MySQL shell")
            print("-" * 50)
            print()
            
        elif choice == "4":
            print("Terima kasih! Sampai jumpa.")
            break
            
        else:
            print("Pilihan tidak valid. Silakan pilih 1-4.")
            print()


if __name__ == "__main__":
    main()
