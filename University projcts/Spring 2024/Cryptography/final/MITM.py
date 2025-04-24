import itertools

# Define permutations and tables used in SDES
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

def permute(bits, table):
    return [bits[i - 1] for i in table]

def shift_left(bits, shifts):
    return bits[shifts:] + bits[:shifts]

def key_schedule(key):
    key = permute(key, P10)
    left, right = key[:5], key[5:]
    left = shift_left(left, 1)
    right = shift_left(right, 1)
    k1 = permute(left + right, P8)
    left = shift_left(left, 2)
    right = shift_left(right, 2)
    k2 = permute(left + right, P8)
    return k1, k2

def sbox(input_bits, sbox):
    row = (input_bits[0] << 1) + input_bits[3]
    col = (input_bits[1] << 1) + input_bits[2]
    return [int(x) for x in f"{sbox[row][col]:02b}"]

def feistel(right, subkey):
    right = permute(right, EP)
    temp = [r ^ k for r, k in zip(right, subkey)]
    left, right = temp[:4], temp[4:]
    sbox_out = sbox(left, S0) + sbox(right, S1)
    return permute(sbox_out, P4)

def fk(bits, subkey):
    left, right = bits[:4], bits[4:]
    temp = feistel(right, subkey)
    left = [l ^ t for l, t in zip(left, temp)]
    return left + right

def encrypt(plaintext, k1, k2):
    bits = permute(plaintext, IP)
    bits = fk(bits, k1)
    bits = bits[4:] + bits[:4]
    bits = fk(bits, k2)
    return permute(bits, IP_INV)

def decrypt(ciphertext, k1, k2):
    bits = permute(ciphertext, IP)
    bits = fk(bits, k2)
    bits = bits[4:] + bits[:4]
    bits = fk(bits, k1)
    return permute(bits, IP_INV)

def to_bits(n, length=8):
    return [int(x) for x in f"{n:0{length}b}"]

def from_bits(bits):
    return int("".join(map(str, bits)), 2)

# Given plaintext-ciphertext pairs
plaintexts = [
    to_bits(0b11110001),
    to_bits(0b00110001),
    to_bits(0b11101101),
    to_bits(0b00101011),
]

ciphertexts = [
    to_bits(0b10101011),
    to_bits(0b00011111),
    to_bits(0b01100011),
    to_bits(0b11010111),
]

# Meet-in-the-Middle attack
matching_keys = []

for a in range(1024):
    key1 = to_bits(a, 10)
    k1_1, k1_2 = key_schedule(key1)
    
    for p, c in zip(plaintexts, ciphertexts):
        midcipher1 = encrypt(p, k1_1, k1_2)
        
        all_match = True
        for b in range(1024):
            key2 = to_bits(b, 10)
            k2_1, k2_2 = key_schedule(key2)
            
            midcipher2 = decrypt(c, k2_2, k2_1)
            
            if midcipher1 != midcipher2:
                all_match = False
                break
        
        if all_match:
            matching_keys.append((key1, key2))

# Output the results
if matching_keys:
    print("Common matching keys found:")
    for k1, k2 in matching_keys:
        print(f"{from_bits(k1):010b} {from_bits(k2):010b}")
else:
    print("No common matching keys found.")
