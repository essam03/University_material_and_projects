import io
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import numpy as np

# Load the image
image_path = r'D:\Univercity\spring 2024 semester\crypto\final\TUX.jpg'
original_image = Image.open(image_path)
original_image_size = original_image.size

# Get the pixel data from the image
image_data = np.array(original_image.convert('RGB'))  # Convert to RGB to ensure no alpha channel
image_data_bytes = image_data.tobytes()
original_image_data_size = len(image_data_bytes)

# Define the key
key = b'Sixteen byte key'  # 16-byte key for AES-128

# Encryption using ECB mode
def encrypt_ecb(plaintext, key):
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = b''
    for i in range(0, len(padded_data), AES.block_size):
        block = padded_data[i:i+AES.block_size]
        encrypted_block = cipher_ecb.encrypt(block)
        ciphertext += encrypted_block
    return ciphertext

# Decryption using ECB mode
def decrypt_ecb(ciphertext, key):
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    decrypted_data = b''
    for i in range(0, len(ciphertext), AES.block_size):
        block = ciphertext[i:i + AES.block_size]
        decrypted_block = cipher_ecb.decrypt(block)
        decrypted_data += decrypted_block    
    return unpad(decrypted_data, AES.block_size)

# Encrypt the pixel data
ciphertext = encrypt_ecb(image_data_bytes, key)

# Save the encrypted image data to a file
encrypted_image_path = r'D:\Univercity\spring 2024 semester\crypto\final\EBC\encrypted_image.bin'
with open(encrypted_image_path, 'wb') as f:
    f.write(ciphertext)

# Decrypt the pixel data
decrypted_data = decrypt_ecb(ciphertext, key)

# Reshape the decrypted data to match the original image dimensions
decrypted_image_data = np.frombuffer(decrypted_data, dtype=np.uint8).reshape(image_data.shape)

# Convert to PIL image and save
decrypted_image = Image.fromarray(decrypted_image_data, mode='RGB')
decrypted_image_path = r'D:\Univercity\spring 2024 semester\crypto\final\EBC\decrypted_image_ecb.jpg'
decrypted_image.save(decrypted_image_path, 'JPEG')

# Show the images
original_image.show(title="Original Image")
decrypted_image.show(title="Decrypted Image (Visualized as JPEG)")

# Reshape the encrypted data to match the original image size for visualization
encrypted_image_data = np.frombuffer(ciphertext, dtype=np.uint8)
encrypted_image_data = encrypted_image_data[:image_data.size].reshape(image_data.shape)

# Convert the encrypted data to an RGB image
encrypted_image = Image.fromarray(encrypted_image_data, mode='RGB')

# Save the encrypted image to verify the process
encrypted_image_jpg_path = r'D:\Univercity\spring 2024 semester\crypto\final\EBC\encrypted_image_ecb.jpg'
encrypted_image.save(encrypted_image_jpg_path, 'JPEG')

# Show the encrypted image
encrypted_image.show(title="Encrypted Image (Visualized as JPEG)")
