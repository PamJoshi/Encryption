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

def get_base_path():
    """Get the base path for the encryption project."""
    return os.environ.get('ENCRYPTION_BASE_PATH', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

def derive_key(key_string):
    """Derive a key from the input string using SHA-256."""
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key_string.encode())
    return base64.urlsafe_b64encode(digest.finalize()[:32])

def encrypt_file(file_path, output_path=None, key_string=None):
    """Encrypt a file using Blowfish algorithm.
    
    Args:
        file_path (str): Path to the file to encrypt
        output_path (str, optional): Directory to save encrypted file. 
                                     Defaults to Encrypted_files/blowfish relative to base path.
        key_string (str, optional): Encryption key. Prompts if not provided.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Resolve base path
    base_path = get_base_path()

    # If no output path provided, use default
    if output_path is None:
        output_path = os.path.join(base_path, 'Encrypted_files', 'blowfish')

    # If no key provided, prompt user
    if key_string is None:
        key_string = input("Enter the encryption key: ")

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Derive key
    key = derive_key(key_string)

    # Read file
    with open(file_path, 'rb') as f:
        data = f.read()

    # Prepare cipher
    iv = os.urandom(8)  # Blowfish block size is 8 bytes
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad data
    padder = padding.PKCS7(algorithms.Blowfish.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Construct output file path
    output_file_name = os.path.basename(file_path) + '.enc'
    output_file_path = os.path.join(output_path, output_file_name)

    # Write encrypted file with IV
    with open(output_file_path, 'wb') as f:
        f.write(iv)  # Write IV first
        f.write(encrypted_data)

if __name__ == "__main__":
    # Use dynamic path resolution
    base_path = get_base_path()
    files_path = os.path.join(base_path, 'Original_files', 'blowfish')
    output_path = os.path.join(base_path, 'Encrypted_files', 'blowfish')
    key_string = input("Enter the encryption key: ")

    for root, dirs, files in os.walk(files_path):
        for file in files:
            file_to_encrypt = os.path.join(root, file)
            encrypt_file(file_to_encrypt, output_path, key_string)
