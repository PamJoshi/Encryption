import os
import warnings
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

# Suppress specific deprecation warning
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

def derive_key(key_string):
    """Derive a key from the input string using SHA-256."""
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key_string.encode())
    return base64.urlsafe_b64encode(digest.finalize()[:32])

def decrypt_file(encrypted_file_path, output_path, key_string):
    
    if not os.path.exists(encrypted_file_path):
        print(f"File not found: {encrypted_file_path}")
        return

    os.makedirs(output_path, exist_ok=True)  # Create output directory if needed

    key = derive_key(key_string)

    try:
        with open(encrypted_file_path, 'rb') as f:
            iv = f.read(8)  # Read the 8-byte initialization vector
            encrypted_data = f.read()

        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.Blowfish.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        # Construct the output file path
        output_file_name = os.path.basename(encrypted_file_path).replace('.enc', '')
        output_file_path = os.path.join(output_path, output_file_name)

        with open(output_file_path, 'wb') as f:
            f.write(decrypted_data)

        print(f"Successfully decrypted {encrypted_file_path} to {output_file_path}")

    except ValueError as e:
        print(f"Incorrect key or corrupted data for file {encrypted_file_path}: {e}")
    except Exception as e:
        print(f"An error occurred during decryption for file {encrypted_file_path}: {e}")

if __name__ == "__main__":
    encrypted_files_path = "D:\\Desktop\\Encryption\\Encrypted_files\\blowfish"
    output_path = "D:\\Desktop\\Encryption\\Decrypted_files\\blowfish"
    key_string = input("Enter the decryption key: ")

    for root, dirs, files in os.walk(encrypted_files_path):
        for file in files:
            if file.endswith('.enc'):
                encrypted_file_path = os.path.join(root, file)
                decrypt_file(encrypted_file_path, output_path, key_string)
