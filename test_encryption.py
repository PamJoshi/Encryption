import os
import pytest
import requests

# Configuration
BASE_URL = "http://localhost:8000"
TEST_FILE_PATH = "Original_files/test_file.txt"
ENCRYPTED_FILE_PATH = "Encrypted_files/encrypted_test_file.enc"

def test_generate_key():
    """Test key generation endpoint"""
    response = requests.get(f"{BASE_URL}/generate-key")
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
    assert "algorithm" in data

def test_file_encryption():
    """Test file encryption endpoint"""
    # Ensure test file exists
    os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)
    with open(TEST_FILE_PATH, 'w') as f:
        f.write("This is a test file for encryption")
    
    # Generate a key
    key_response = requests.get(f"{BASE_URL}/generate-key")
    key = key_response.json()['key']
    
    # Encrypt file
    with open(TEST_FILE_PATH, 'rb') as f:
        files = {'file': f}
        data = {
            'algorithm': 'aes256',
            'key': key,
            'input_path': TEST_FILE_PATH,
            'output_path': ENCRYPTED_FILE_PATH
        }
        response = requests.post(f"{BASE_URL}/encrypt", files=files, data=data)
    
    # Assertions
    assert response.status_code == 200
    result = response.json()
    assert result['original_file'] == TEST_FILE_PATH
    assert result['encrypted_file'] == ENCRYPTED_FILE_PATH
    assert result['algorithm'] == 'aes256'
    assert os.path.exists(ENCRYPTED_FILE_PATH)

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'

if __name__ == "__main__":
    pytest.main() 