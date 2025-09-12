import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def get_base_path():
    """Get the base path for the encryption project."""
    return os.environ.get('ENCRYPTION_BASE_PATH', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

def encrypt_file(file_path, output_path=None, key_string=None):
    """Encrypts a file using AES-128 and saves it to a specific path.
    
    Args:
        file_path (str): Path to the file to encrypt
        output_path (str, optional): Directory to save encrypted file. 
                                     Defaults to Encrypted_files/aes128 relative to base path.
        key_string (str, optional): Encryption key. Prompts if not provided.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Resolve base path
    base_path = get_base_path()

    # If no output path provided, use default
    if output_path is None:
        output_path = os.path.join(base_path, 'Encrypted_files', 'aes128')

    # If no key provided, prompt user
    if key_string is None:
        key_string = input("Enter the encryption key: ")

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Derive a 32-byte key from the input string
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key_string.encode())
    key = base64.urlsafe_b64encode(digest.finalize())

    fernet = Fernet(key)

    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    # Construct the output file path
    output_file_name = os.path.basename(file_path) + '.enc'
    output_file_path = os.path.join(output_path, output_file_name)

    with open(output_file_path, 'wb') as f:
        f.write(encrypted_data)

if __name__ == "__main__":
    # Use dynamic path resolution
    base_path = get_base_path()
    file_path = os.path.join(base_path, 'Original_files', 'aes128')
    output_path = os.path.join(base_path, 'Encrypted_files', 'aes128')
    key_string = input("Enter the encryption key: ")

    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_to_encrypt = os.path.join(root, file)
            encrypt_file(file_to_encrypt, output_path, key_string)
