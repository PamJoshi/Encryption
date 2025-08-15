import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import padding as sym_padding  # Correct import
from cryptography.hazmat.backends import default_backend

def load_private_key(private_key_path):
    """Load the RSA private key from a file."""
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
    return private_key

def decrypt_file(file_path, output_path, private_key, password):
    """Decrypt a file using RSA and a password-derived symmetric key."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    os.makedirs(output_path, exist_ok=True)

    # Read the encrypted file contents
    with open(file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        encrypted_symmetric_key = f.read(256)
        encrypted_data = f.read()

    # Decrypt the symmetric key using the RSA private key
    symmetric_key = private_key.decrypt(
        encrypted_symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt the file contents with AES-256 using the derived symmetric key
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the data
    unpadder = sym_padding.PKCS7(128).unpadder()  # Correct padding unpadder
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    # Construct the output file path by removing the '.enc' extension
    output_file_name = os.path.basename(file_path).replace('.enc', '')
    output_file_path = os.path.join(output_path, output_file_name)

    with open(output_file_path, 'wb') as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    input_path = "D:\\Desktop\\Encryption\\Encrypted_files\\rsa"
    output_path = "D:\\Desktop\\Encryption\\Decrypted_files\\rsa"
    private_key_path = "D:\\Desktop\\Encryption\\Keys\\private_key.pem"

    # Load the private key for decryption
    private_key = load_private_key(private_key_path)

    # Ask the user for the decryption password
    password = input("Enter the decryption password: ")

    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith('.enc'):
                file_to_decrypt = os.path.join(root, file)
                decrypt_file(file_to_decrypt, output_path, private_key, password)
