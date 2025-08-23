import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def get_base_path():
    """Get the base path for the encryption project."""
    return os.environ.get('ENCRYPTION_BASE_PATH', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

def generate_rsa_keys(keys_path=None):
    """Generate RSA keys.
    
    Args:
        keys_path (str, optional): Path to save keys. 
                                   Defaults to Keys directory in base path.
    """
    # Resolve base path
    base_path = get_base_path()

    # If no keys path provided, use default
    if keys_path is None:
        keys_path = os.path.join(base_path, 'Keys')

    # Ensure keys directory exists
    os.makedirs(keys_path, exist_ok=True)

    # Generate keys
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Serialize and save private key
    private_key_path = os.path.join(keys_path, 'private_key.pem')
    with open(private_key_path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Serialize and save public key
    public_key_path = os.path.join(keys_path, 'public_key.pem')
    with open(public_key_path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key, public_key

def encrypt_private_key(private_key, password):
    """Encrypt the RSA private key using AES-256."""
    salt = os.urandom(16)
    iv = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Pad private key to block size
    padding_length = (16 - len(private_key_bytes) % 16) % 16
    padded_private_key = private_key_bytes + b'\0' * padding_length
    encrypted_private_key = encryptor.update(padded_private_key) + encryptor.finalize()

    return salt, iv, encrypted_private_key

def encrypt_file(file_path, output_path=None, public_key=None, password=None):
    """Encrypt the file and include the encrypted private key.
    
    Args:
        file_path (str): Path to the file to encrypt
        output_path (str, optional): Directory to save encrypted file. 
                                     Defaults to Encrypted_files/rsa relative to base path.
        public_key (object, optional): RSA public key. Loads from file if not provided.
        password (str, optional): Password for private key encryption. Prompts if not provided.
    """
    # Resolve base path
    base_path = get_base_path()

    # If no output path provided, use default
    if output_path is None:
        output_path = os.path.join(base_path, 'Encrypted_files', 'rsa')

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Load public key if not provided
    if public_key is None:
        public_key_path = os.path.join(base_path, 'Keys', 'public_key.pem')
        with open(public_key_path, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

    # Generate symmetric key for file encryption
    symmetric_key = os.urandom(32)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Read and encrypt file data
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Pad file data to block size
    padding_length = (16 - len(file_data) % 16) % 16
    padded_file_data = file_data + b'\0' * padding_length
    encrypted_file_data = encryptor.update(padded_file_data) + encryptor.finalize()

    # Encrypt the symmetric key with RSA public key
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Construct the output file path
    output_file_name = os.path.basename(file_path) + '.enc'
    output_file_path = os.path.join(output_path, output_file_name)

    # Write everything to the output file: iv, encrypted symmetric key, encrypted file data
    with open(output_file_path, 'wb') as f:
        f.write(iv)
        f.write(encrypted_symmetric_key)
        f.write(encrypted_file_data)

if __name__ == "__main__":
    # Use dynamic path resolution
    base_path = get_base_path()
    
    # Generate keys
    generate_rsa_keys()

    # Encrypt files
    file_path = os.path.join(base_path, 'Original_files', 'rsa')
    output_path = os.path.join(base_path, 'Encrypted_files', 'rsa')
    
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_to_encrypt = os.path.join(root, file)
            encrypt_file(file_to_encrypt, output_path)
