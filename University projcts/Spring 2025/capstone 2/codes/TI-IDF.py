import sqlite3
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🔧 Normalize user .asm file
def normalize_assembly(code_text):
    lines = code_text.splitlines()
    normalized = []

    for line in lines:
        line = re.sub(r';.*', '', line).strip().lower()
        # Skip non-instruction lines
        if not line or any(keyword in line for keyword in ['section', 'global', '.text', '.data', '_start:', 'input db']):
            continue
        # Normalize register names, variables, and constants
        line = re.sub(r'\b(e?[abcd]x|esi|edi|ebp|esp|r\d+|input|buffer|data|buf|ptr)\b', 'REG', line)
        line = re.sub(r'0x[0-9a-f]+|\b\d+\b', 'IMM', line)
        line = re.sub(r'\b(call|jmp|je|jne|jz|jnz)\s+\w+', r'\1 FUNC', line)
        normalized.append(line)

    return ' '.join(normalized)

# 🔧 Normalize pseudo-code / custom pattern entries
def normalize_custom(text):
    replacements = [
        (r'call compare with .*', 'call FUNC'),
        (r'test result', 'test REG, REG'),
        (r'jump if equal to .*', 'je FUNC'),
        (r'set month index', 'mov REG, IMM'),
        (r'proceed to parse .*', 'call FUNC'),
        (r'return error', 'mov REG, IMM\nret'),
        (r'return', 'ret'),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

# 📥 Load patterns from SQLite DB
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

# 📊 Perform comparison between user file and DB patterns
def compare_user_code(user_code_text, db_patterns, threshold=0.4):
    user_normalized = normalize_assembly(user_code_text)
    db_normalized = [
        normalize_assembly(normalize_custom(p['assembly'])) for p in db_patterns
    ]

    print("\n🔍 USER Normalized Assembly:")
    print(user_normalized)

    print("\n🔍 First 5 DB Normalized Patterns:")
    for i, code in enumerate(db_normalized[:5]):
        print(f"Pattern {db_patterns[i]['id']} ({db_patterns[i]['title']}): {code}")

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_normalized] + db_normalized)

    user_vec = tfidf_matrix[0]
    db_vecs = tfidf_matrix[1:]

    similarities = cosine_similarity(user_vec, db_vecs).flatten()

    print("\n🟨 Normalized DB Patterns and Similarity Scores:")
    results = []
    for idx, score in enumerate(similarities):
        pattern = db_patterns[idx]
        print(f"- Pattern {pattern['id']} ({pattern['title']}): {score:.3f}")
        if score >= threshold:
            results.append({
                'pattern_id': pattern['id'],
                'title': pattern['title'],
                'category': pattern['category'],
                'attack_type': pattern['attack_type'],
                'similarity': round(float(score), 3)
            })
    return results

# 🚀 Entry Point
if __name__ == '__main__':
    user_code_path = "C:/Users/User/Downloads/buffer_overflow_test.asm"
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
            print(f"[{m['similarity']*100:.1f}% match] {m['title']} ({m['category']}) - {m['attack_type']}")
