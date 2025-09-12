#!/usr/bin/env python3
"""
Simple test script to verify encryption functionality works
"""
import os
import tempfile
from Process.Symmetric_algo.Encryption_algo.aes256 import encrypt_file as aes256_encrypt

def test_aes256_encryption():
    """Test AES256 encryption with a simple file"""
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as test_file:
        test_file.write("This is a test file for encryption.")
        test_file_path = test_file.name
    
    try:
        # Create temporary output directory
        output_dir = tempfile.mkdtemp()
        
        # Test encryption
        print(f"Testing AES256 encryption...")
        print(f"Input file: {test_file_path}")
        print(f"Output directory: {output_dir}")
        
        # Call encryption function
        aes256_encrypt(test_file_path, output_dir, "test_key_123")
        
        # Check if encrypted file was created
        encrypted_files = os.listdir(output_dir)
        if encrypted_files:
            encrypted_file_path = os.path.join(output_dir, encrypted_files[0])
            print(f"✅ Encryption successful! Created: {encrypted_file_path}")
            
            # Check file size
            original_size = os.path.getsize(test_file_path)
            encrypted_size = os.path.getsize(encrypted_file_path)
            print(f"Original file size: {original_size} bytes")
            print(f"Encrypted file size: {encrypted_size} bytes")
            
            return True
        else:
            print("❌ No encrypted file was created")
            return False
            
    except Exception as e:
        print(f"❌ Encryption failed with error: {str(e)}")
        return False
    finally:
        # Clean up
        if os.path.exists(test_file_path):
            os.unlink(test_file_path)

if __name__ == "__main__":
    print("Testing encryption functionality...")
    success = test_aes256_encryption()
    if success:
        print("\n🎉 Encryption test passed!")
    else:
        print("\n💥 Encryption test failed!")