import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def get_base_path():
    """Get the base path for the encryption project."""
    return os.environ.get('ENCRYPTION_BASE_PATH', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

def decrypt_file(input_path, output_path=None, key_string=None):
    """Decrypts a file using AES-256 and saves it to a specific path.
    
    Args:
        input_path (str): Path to the encrypted file
        output_path (str, optional): Directory to save decrypted file. 
                                     Defaults to Decrypted_files/aes256 relative to base path.
        key_string (str, optional): Decryption key. Prompts if not provided.
    """
    # Resolve base path
    base_path = get_base_path()

    # If no output path provided, use default
    if output_path is None:
        output_path = os.path.join(base_path, 'Decrypted_files', 'aes256')

    # If no key provided, prompt user
    if key_string is None:
        key_string = input("Enter the decryption key: ")

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Derive a key from the input string
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key_string.encode())
    key = base64.urlsafe_b64encode(digest.finalize()[:32])

    fernet = Fernet(key)

    # Read encrypted file
    with open(input_path, 'rb') as f:
        encrypted_data = f.read()

    # Decrypt data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print(f"Decryption failed: {e}")
        return

    # Construct the output file path
    output_file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_file_path = os.path.join(output_path, output_file_name)

    # Write decrypted file
    with open(output_file_path, 'wb') as f:
        f.write(decrypted_data)

    print(f"Decrypted {input_path} and saved to {output_file_path}")

if __name__ == "__main__":
    # Use dynamic path resolution
    base_path = get_base_path()
    input_path = os.path.join(base_path, 'Encrypted_files', 'aes256')
    output_path = os.path.join(base_path, 'Decrypted_files', 'aes256')
    key_string = input("Enter the decryption key: ")

    # Decrypt all files in the input directory
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith('.enc'):
                file_to_decrypt = os.path.join(root, file)
                decrypt_file(file_to_decrypt, output_path, key_string)
