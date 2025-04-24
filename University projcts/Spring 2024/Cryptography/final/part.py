def main():
    # Plaintext and ciphertext pairs
    pairs = [
        ([1, 1, 1, 1, 0, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1, 1]),  # P1: 11110001, C1: 10101011
        ([0, 0, 1, 1, 0, 0, 0, 1], [0, 0, 0, 1, 1, 1, 1, 1]),  # P2: 00110001, C2: 00011111
        ([1, 1, 1, 0, 1, 1, 0, 1], [0, 1, 1, 0, 0, 0, 1, 1]),  # P3: 11101101, C3: 01100011
        ([0, 0, 1, 0, 1, 0, 1, 1], [1, 1, 0, 1, 0, 1, 1, 1])   # P4: 00101011, C4: 11010111
    ]

    found_keys = meet_in_the_middle_attack(pairs)
    if found_keys:
        print(f"Found key pairs that work for all traces: {found_keys}")
    else:
        print("No key pairs found that work for all traces.")

def meet_in_the_middle_attack(pairs):
    for key1 in range(1024):
        for key2 in range(1024):
            key1_bits = int_to_bits(key1, 10)
            key2_bits = int_to_bits(key2, 10)
            
            k1_1 = generate_subkey(key1, 1)
            k2_1 = generate_subkey(key1, 2)
            k3_2 = generate_subkey(key2, 3)
            k4_2 = generate_subkey(key2, 4)

            all_match = True
            for plaintext, expected_ciphertext in pairs:
                # Encrypt with first key pair
                intermediate = encrypt(k1_1, k2_1, plaintext)

                # Decrypt with second key pair
                decrypted_intermediate = decrypt(k4_2, k3_2, expected_ciphertext)

                if intermediate != decrypted_intermediate:
                    all_match = False
                    break
            
            if all_match:
                return (key1, key2)

    return None

def int_to_bits(value, bit_length):
    return [int(bit) for bit in f"{value:0{bit_length}b}"]

def generate_subkey(key, round):
    key_bits = int_to_bits(key, 10)
    new_key = p10(key_bits)
    split_l = new_key[:5]
    split_r = new_key[5:]

    shift_amount = round
    split_l = shift_left(split_l, shift_amount)
    split_r = shift_left(split_r, shift_amount)

    combined_key = split_l + split_r
    return p8(combined_key)

def encrypt(k1, k2, plaintext):
    permuted = initial_permutation(plaintext)
    intermediate1 = fk_round(permuted, k1)
    intermediate2 = fk_round(intermediate1, k2)
    return final_permutation(intermediate2)

def decrypt(k2, k1, ciphertext):
    permuted = initial_permutation(ciphertext)
    intermediate2 = fk_round(permuted, k2)
    intermediate1 = fk_round(intermediate2, k1)
    return final_permutation(intermediate1)

def fk_round(input, key):
    left = input[:4]
    right = input[4:]

    round_output = fk(left, right, key)
    swapped = swap_halves(round_output)

    left = swapped[:4]
    right = swapped[4:]

    return fk(left, right, key)

def fk(left, right, key):
    ep = EP(right)
    xor_output = xor(ep, key)

    sbox_output = sboxes(xor_output)

    p4_output = p4(sbox_output)
    new_left = xor(left, p4_output)

    return new_left + right

def xor(a, b):
    return [a[i] ^ b[i] for i in range(len(a))]

def swap_halves(input):
    half_length = len(input) // 2
    return input[half_length:] + input[:half_length]

def initial_permutation(input):
    return [input[1], input[5], input[2], input[0], input[3], input[7], input[4], input[6]]

def final_permutation(input):
    return [input[3], input[0], input[2], input[4], input[6], input[1], input[7], input[5]]

def p10(key):
    return [key[2], key[4], key[1], key[6], key[3], key[9], key[0], key[8], key[7], key[5]]

def p8(key):
    return [key[5], key[2], key[6], key[3], key[7], key[4], key[9], key[8]]

def p4(input):
    return [input[1], input[3], input[2], input[0]]

def EP(right):
    return [right[3], right[0], right[1], right[2], right[1], right[2], right[3], right[0]]

def shift_left(bits, num_shifts):
    return bits[num_shifts:] + bits[:num_shifts]

def sboxes(input):
    left = input[:4]
    right = input[4:]

    sbox_output = [0] * 4
    sbox_output[:2] = s0(left)
    sbox_output[2:] = s1(right)
    return sbox_output

def s0(input):
    s0_matrix = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]

    row = (input[0] << 1) + input[3]
    col = (input[1] << 1) + input[2]
    value = s0_matrix[row][col]

    return [(value >> 1) & 1, value & 1]

def s1(input):
    s1_matrix = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]

    row = (input[0] << 1) + input[3]
    col = (input[1] << 1) + input[2]
    value = s1_matrix[row][col]

    return [(value >> 1) & 1, value & 1]

if __name__ == "__main__":
    main()
