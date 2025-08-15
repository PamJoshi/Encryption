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
    file_path = os.path.join(temp_dir, "encrypted", filename)
    
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename, media_type='application/octet-stream')
    
    raise HTTPException(status_code=404, detail="File not found")

# Decryption route (similar structure can be added)
@app.post("/decrypt")
async def decrypt_file():
    # TODO: Implement decryption logic similar to encryption
    raise HTTPException(status_code=501, detail="Decryption not yet implemented")

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