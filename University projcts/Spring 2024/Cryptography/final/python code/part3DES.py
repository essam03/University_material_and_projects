from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# AES CBC encryption function
def encrypt(message, key):
    key = bytes.fromhex(key)  # Convert key from hex string to bytes
    cipher = AES.new(key, AES.MODE_CBC)         # Create a new AES cipher object in CBC mode. A random IV is generated here.
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

# AES CBC decryption function
def decrypt(iv, ct, key):
    key = bytes.fromhex(key)  # Convert key from hex string to bytes
    ct = base64.b64decode(ct)
    iv = base64.b64decode(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

# Example usage:
if __name__ == '__main__':
    key = "00112233445566778899aabbccddeeff"  # 16-byte (32-character) hexadecimal key
    message =input("write your message! " + "") 

    iv, ciphertext = encrypt(message, key)
    print(f"IV: {iv}")
    print(f"Ciphertext: {ciphertext}")

    plaintext = decrypt(iv, ciphertext, key)
    print(f"Decrypted plaintext: {plaintext}")
