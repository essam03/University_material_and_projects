import sqlite3

# ✅ Update this to your SHA256 file path
file_path = r'C:\Users\User\Downloads\Malware-Hash-Database-main\SHA256\sha256_hashes_6.txt'
db_path = r'D:\Univercity\Spring 2025\Capstone Project II\Bughex DB\bughex.db'

def insert_hashes(txt_file, db_path, hash_type):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hashes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            hash_type TEXT,
            Hash TEXT UNIQUE
        )
    ''')

    with open(txt_file, 'r') as f:
        for line in f:
            hash_val = line.strip()
            if hash_val:
                cursor.execute('''
                    INSERT OR IGNORE INTO hashes (hash_type, Hash)
                    VALUES (?, ?)
                ''', (hash_type.upper(), hash_val))

    conn.commit()
    conn.close()
    print(f"[+] Inserted {hash_type.upper()} hashes from {txt_file} into {db_path} (duplicates ignored).")

# 👇 Insert SHA256 hashes
insert_hashes(file_path, db_path, 'SHA256')
