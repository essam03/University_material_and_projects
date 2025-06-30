import re
import json
import os
import sqlite3

def parse_cfg(file_path):
    cfg = {}
    instr_pattern = re.compile(r"^(0x[0-9a-fA-F]+):\s+(.+)$")

    with open(file_path, 'r') as f:
        for line in f:
            match = instr_pattern.match(line.strip())
            if match:
                addr, instr = match.groups()
                if addr not in cfg:
                    cfg[addr] = {'instruction': instr, 'edges': []}

                instr_lower = instr.lower()
                if instr_lower.startswith(('jmp ', 'call ')):
                    parts = instr_lower.split()
                    if len(parts) == 2 and parts[1].startswith('0x'):
                        cfg[addr]['edges'].append(parts[1])
                elif instr_lower.startswith(('ret', 'hlt')):
                    cfg[addr]['edges'].append('END')
    return cfg

def normalize_asm(code_text):
    lines = code_text.splitlines()
    normalized = []
    for line in lines:
        line = re.sub(r';.*', '', line).strip().lower()
        if not line or any(k in line for k in ['section', 'global', '.text', '.data', '_start:', 'input db']):
            continue
        line = re.sub(r'\b(e?[abcd]x|esi|edi|ebp|esp|r\d+|input|buffer|data|buf|ptr)\b', 'REG', line)
        line = re.sub(r'0x[0-9a-f]+|\b\d+\b', 'IMM', line)
        normalized.append(line)
    return ' '.join(normalized)

def save_to_sqlite(file_name, normalized_code, cfg_dict, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS malware_cfg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            normalized_code TEXT,
            cfg_json TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO malware_cfg (file_name, normalized_code, cfg_json)
        VALUES (?, ?, ?)
    ''', (file_name, normalized_code, json.dumps(cfg_dict)))

    conn.commit()
    conn.close()
    print(f"✅ Saved CFG for {file_name} to DB.")

# === Main ===
if __name__ == '__main__':
    input_path = "C:\\Users\\User\\Downloads\\disassembly_output1.asm"
    db_path = "D:/Univercity/Spring 2025/Capstone Project II/Bughex DB/bughex.db"

    if not os.path.exists(input_path):
        print("❌ File not found")
    else:
        with open(input_path, 'r') as f:
            code = f.read()

        cfg = parse_cfg(input_path)
        norm_code = normalize_asm(code)
        save_to_sqlite(os.path.basename(input_path), norm_code, cfg, db_path)
