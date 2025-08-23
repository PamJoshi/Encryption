import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def decrypt_file(file_path, output_path, key_string):
    

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    os.makedirs(output_path, exist_ok=True)  # Create output directory if needed

    # Derive a 32-byte key from the input string
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key_string.encode())
    key = base64.urlsafe_b64encode(digest.finalize())

    fernet = Fernet(key)

    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()   

        decrypted_data = fernet.decrypt(encrypted_data)

        # Construct the output file path
        output_file_name = os.path.basename(file_path)[:-4]  # Remove '.enc' extension
        output_file_path = os.path.join(output_path, output_file_name)

        with open(output_file_path, 'wb') as f:
            f.write(decrypted_data)

    except InvalidToken:
        print(f"Incorrect decryption key for file: {file_path}")

if __name__ == "__main__":
    input_path = "D:\\Desktop\\Encryption\\Encrypted_files\\aes128"
    output_path = "D:\\Desktop\\Encryption\\Decrypted_files\\aes128"
    key_string = input("Enter the decryption key: ")

    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith('.enc'):
                file_to_decrypt = os.path.join(root, file)
                decrypt_file(file_to_decrypt, output_path, key_string)
