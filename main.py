import os
import tempfile
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import base64

# Import existing encryption modules
from Process.Symmetric_algo.Encryption_algo.aes256 import encrypt_file as aes256_encrypt
from Process.Symmetric_algo.Encryption_algo.aes128 import encrypt_file as aes128_encrypt
from Process.Symmetric_algo.Encryption_algo.blowfish import encrypt_file as blowfish_encrypt
from Process.Asymmetric_algo.Encryption.rsa.rsa import encrypt_file as rsa_encrypt

# Create FastAPI app
app = FastAPI(
    title="Encryption Service",
    description="Comprehensive Encryption API for Various Algorithms",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for friendly landing page
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Encryption Service API!",
        "docs": "/docs",
        "endpoints": ["/encrypt", "/decrypt", "/generate-key", "/health", "/docs"]
    }

# Encryption algorithm types
class EncryptionAlgorithm:
    AES256 = "aes256"
    AES128 = "aes128"
    BLOWFISH = "blowfish"
    RSA = "rsa"

# Encryption response model
class EncryptionResponse(BaseModel):
    original_file: str
    encrypted_file: str
    algorithm: str
    message: str

# Encryption route - Updated to handle file uploads
@app.post("/encrypt", response_model=EncryptionResponse)
@app.post("/api/encrypt", response_model=EncryptionResponse)  # Add both endpoints
async def encrypt_file_upload(
    file: UploadFile = File(...),
    algorithm: str = Form(...),
    key: str = Form(...)
):
    try:
        # Validate algorithm
        if algorithm not in [EncryptionAlgorithm.AES256, EncryptionAlgorithm.AES128,
                           EncryptionAlgorithm.BLOWFISH, EncryptionAlgorithm.RSA]:
            raise HTTPException(status_code=400, detail="Unsupported encryption algorithm")
        
        # Create temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Save uploaded file to temporary location
            input_path = os.path.join(temp_dir, file.filename)
            with open(input_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Create output directory (not file path)
            output_dir = os.path.join(temp_dir, "encrypted")
            os.makedirs(output_dir, exist_ok=True)
            
            # Determine encryption algorithm and call with correct parameters
            if algorithm == EncryptionAlgorithm.AES256:
                aes256_encrypt(input_path, output_dir, key)
                output_filename = f"{file.filename}.enc"
            elif algorithm == EncryptionAlgorithm.AES128:
                aes128_encrypt(input_path, output_dir, key)
                output_filename = f"{file.filename}.enc"
            elif algorithm == EncryptionAlgorithm.BLOWFISH:
                blowfish_encrypt(input_path, output_dir, key)
                output_filename = f"{file.filename}.enc"
            elif algorithm == EncryptionAlgorithm.RSA:
                # RSA has different parameters - it needs a password, not a key
                rsa_encrypt(input_path, output_dir, None, key)  # Using key as password
                output_filename = f"{file.filename}.enc"
            
            # Get the actual output file path
            actual_output_path = os.path.join(output_dir, output_filename)
            
            # Check if the encrypted file was created
            if os.path.exists(actual_output_path):
                # Store the temp directory path for later cleanup/download
                download_path = f"/download/{temp_dir.split('/')[-1]}/{output_filename}"
                
                return EncryptionResponse(
                    original_file=file.filename,
                    encrypted_file=download_path,
                    algorithm=algorithm,
                    message="File encrypted successfully"
                )
            else:
                raise HTTPException(status_code=500, detail="Encryption completed but output file not found")
            
        finally:
            # Keep temp files for download - clean up later or implement cleanup mechanism
            pass
    
    except Exception as e:
        # Clean up on error
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")

# Add endpoint to download encrypted files
@app.get("/download/{temp_id}/{filename}")
async def download_file(temp_id: str, filename: str):
    temp_dir = os.path.join(tempfile.gettempdir(), temp_id)
    # Try 'decrypted' subfolder first (for decrypted downloads)
    file_path = os.path.join(temp_dir, 'decrypted', filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename, media_type='application/octet-stream')
    # Then try 'encrypted' subfolder (for encrypted downloads)
    file_path = os.path.join(temp_dir, 'encrypted', filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename, media_type='application/octet-stream')
    raise HTTPException(status_code=404, detail="File not found")

# Decryption response model
class DecryptionResponse(BaseModel):
    original_file: str
    decrypted_file: str
    algorithm: str
    message: str

# Decryption route - handle file uploads
@app.post("/decrypt", response_model=DecryptionResponse)
@app.post("/api/decrypt", response_model=DecryptionResponse)
async def decrypt_file_upload(
    file: UploadFile = File(...),
    algorithm: str = Form(...),
    key: str = Form(...)
):
    try:
        # Validate algorithm
        if algorithm not in [EncryptionAlgorithm.AES256, EncryptionAlgorithm.AES128,
                           EncryptionAlgorithm.BLOWFISH, EncryptionAlgorithm.RSA]:
            raise HTTPException(status_code=400, detail="Unsupported decryption algorithm")

        # Create temporary directory for processing
        temp_dir = tempfile.mkdtemp()

        try:
            # Save uploaded file to temporary location
            input_path = os.path.join(temp_dir, file.filename)
            with open(input_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Create output directory (not file path)
            output_dir = os.path.join(temp_dir, "decrypted")
            os.makedirs(output_dir, exist_ok=True)

            # Determine decryption algorithm and call with correct parameters
            if algorithm == EncryptionAlgorithm.AES256:
                from Process.Symmetric_algo.Decryption_algo.aes256_dec import decrypt_file as aes256_dec
                aes256_dec(input_path, output_dir, key)
                output_filename = os.path.splitext(file.filename)[0]  # Remove .enc
            elif algorithm == EncryptionAlgorithm.AES128:
                from Process.Symmetric_algo.Decryption_algo.aes128_dec import decrypt_file as aes128_dec
                aes128_dec(input_path, output_dir, key)
                output_filename = os.path.splitext(file.filename)[0]
            elif algorithm == EncryptionAlgorithm.BLOWFISH:
                from Process.Symmetric_algo.Decryption_algo.blowfish_dec import decrypt_file as blowfish_dec
                blowfish_dec(input_path, output_dir, key)
                output_filename = file.filename.replace('.enc', '')
            elif algorithm == EncryptionAlgorithm.RSA:
                from Process.Asymmetric_algo.Decryption.rsa.rsa_dec import decrypt_file as rsa_dec, load_private_key
                # For RSA, key is the password, and private key is loaded from file
                base_path = get_base_path() if 'get_base_path' in globals() else os.getcwd()
                private_key_path = os.path.join(base_path, 'Keys', 'private_key.pem')
                private_key = load_private_key(private_key_path)
                rsa_dec(input_path, output_dir, private_key, key)
                output_filename = file.filename.replace('.enc', '')

            # Get the actual output file path
            actual_output_path = os.path.join(output_dir, output_filename)

            # Check if the decrypted file was created
            if os.path.exists(actual_output_path):
                download_path = f"/download/{temp_dir.split('/')[-1]}/{output_filename}"
                return DecryptionResponse(
                    original_file=file.filename,
                    decrypted_file=download_path,
                    algorithm=algorithm,
                    message="File decrypted successfully"
                )
            else:
                raise HTTPException(status_code=500, detail="Decryption completed but output file not found")

        finally:
            # Keep temp files for download - clean up later or implement cleanup mechanism
            pass

    except Exception as e:
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

# Key generation route
@app.get("/generate-key")
async def generate_encryption_key(algorithm: str = EncryptionAlgorithm.AES256, length: int = 32):
    try:
        # Generate a cryptographically secure random key
        key = base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8')
        return {"key": key, "algorithm": algorithm}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Key generation failed: {str(e)}")

# Health check route
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Encryption service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)