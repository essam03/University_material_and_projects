import sqlite3
import re
from sentence_transformers import SentenceTransformer, util

# ✅ Load stronger BERT model
bert_model = SentenceTransformer('all-mpnet-base-v2')

# 🔧 Normalize .asm or pseudo-code
def normalize_assembly(code_text):
    lines = code_text.splitlines()
    normalized = []

    for line in lines:
        line = re.sub(r';.*', '', line).strip().lower()
        if not line or any(k in line for k in ['section', 'global', '.text', '.data', '_start:', 'input db']):
            continue
        line = re.sub(r'\b(e?[abcd]x|esi|edi|ebp|esp|r\d+|input|buffer|data|buf|ptr)\b', 'REG', line)
        line = re.sub(r'0x[0-9a-f]+|\b\d+\b', 'IMM', line)
        line = re.sub(r'mov\s+REG,\s*\[REG.*\]', 'read REG', line)
        line = re.sub(r'mov\s+\[REG.*\],\s*REG', 'write REG', line)
        line = re.sub(r'mov\s+REG,\s*\[.*\+.*\]', 'offset read', line)
        line = re.sub(r'mov\s+\[.*\+.*\],\s*REG', 'offset write', line)
        line = re.sub(r'int\s+0x80', 'syscall', line)
        line = re.sub(r'\bxor\s+REG,\s*REG', 'clear REG', line)
        line = re.sub(r'mov\s+REG,\s*REG', 'copy REG', line)
        line = re.sub(r'mov\s+REG,\s*IMM', 'load REG', line)
        normalized.append(line)

    return ' '.join(normalized)

def normalize_custom(text):
    patterns = [
        (r'call compare with .*', 'call FUNC'),
        (r'test result', 'test REG, REG'),
        (r'jump if equal to .*', 'je FUNC'),
        (r'set month index', 'load REG'),
        (r'proceed to parse .*', 'call FUNC'),
        (r'return error', 'load REG\nret'),
        (r'return', 'ret'),
        (r'move .* to .*', 'load REG'),
        (r'compare .*', 'cmp REG, IMM'),
        (r'clear .*', 'clear REG'),
        (r'read input larger than buffer', 'buffer overflow'),
        (r'input size exceeds buffer', 'buffer overflow'),
        (r'write to input without check', 'unchecked write'),
        (r'loop without bounds', 'infinite loop'),
        (r'offset access without check', 'pointer overflow'),
        (r'use syscall with large edx', 'overflow via syscall'),
        (r'set edx > buffer', 'buffer overflow risk')
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

# 📥 Load patterns from SQLite
def load_patterns_from_sqlite(db_path='bughex.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category, attack_type, assembly_sequence FROM malicious_patterns")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            'id': row[0],
            'title': row[1],
            'category': row[2],
            'attack_type': row[3],
            'assembly': row[4]
        }
        for row in rows
    ]

# 📊 Compare using BERT only
def compare_user_code(user_code_text, db_patterns, threshold=0.45):
    user_norm = normalize_assembly(normalize_custom(user_code_text))
    db_norms = [normalize_assembly(normalize_custom(p['assembly'])) for p in db_patterns]

    print("\n🔍 USER Normalized Assembly:")
    print(user_norm)

    user_vec = bert_model.encode(user_norm, convert_to_tensor=True)
    db_vecs = bert_model.encode(db_norms, convert_to_tensor=True)

    similarities = util.cos_sim(user_vec, db_vecs)[0].cpu().numpy()

    results = []
    for idx, score in enumerate(similarities):
        if score >= threshold:
            pattern = db_patterns[idx]
            risk = "🔴 High" if score > 0.75 else "🟠 Medium" if score > 0.5 else "🟢 Low"
            results.append({
                'pattern_id': pattern['id'],
                'title': pattern['title'],
                'category': pattern['category'],
                'attack_type': pattern['attack_type'],
                'similarity': round(float(score), 3),
                'risk': risk
            })
    return results

# 🚀 Main
if __name__ == '__main__':
    user_code_path = "C:/Users/User/Downloads/safe_read.asm"
    db_path = "D:/Univercity/Spring 2025/Capstone Project II/Bughex DB/bughex.db"

    with open(user_code_path, 'r') as f:
        user_asm_code = f.read()

    patterns = load_patterns_from_sqlite(db_path)
    matches = compare_user_code(user_asm_code, patterns)

    print("\n🟢 Results:")
    if not matches:
        print("No significant similarity found.")
    else:
        for m in matches:
            print(f"[{m['similarity']*100:.1f}% match] {m['title']} ({m['category']}) - {m['attack_type']} [{m['risk']}]")
