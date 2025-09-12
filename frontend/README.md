# Encryption Service with FastAPI & React Frontend

## Overview
A comprehensive encryption service featuring a FastAPI backend and React frontend, supporting multiple encryption algorithms including AES-128, AES-256, Blowfish, and RSA. The service provides a modern web interface for file encryption with real-time processing and secure file downloads.

## Features

### Backend (FastAPI)
- **RESTful API** for file encryption/decryption
- **File upload support** with multipart/form-data handling
- **Multiple encryption algorithms**: AES-128, AES-256, Blowfish, RSA
- **Key generation endpoint** with cryptographically secure random keys
- **File download system** for encrypted files
- **CORS enabled** for frontend communication
- **Swagger UI documentation** at `/docs`
- **Health check endpoint** for service monitoring

### Frontend (React + Material UI)
- **Modern, responsive web interface** with Material UI components
- **File upload** with drag-and-drop functionality
- **Real-time encryption status** and progress feedback
- **Download encrypted files** directly from the browser
- **Key generation interface** with algorithm selection
- **Multi-page navigation**: Encrypt, Decrypt, Key Generation, Health Check
- **API documentation access** via integrated link

## Prerequisites
- **Python 3.10+**
- **Node.js 16+** and npm/yarn
- **Docker** (optional, for containerized deployment)

## Quick Start

### Option 1: Docker Setup (Recommended)
```bash
# Start the backend service
docker-compose up --build -d

# Install and start frontend
cd frontend
npm install
npm run dev
```

### Option 2: Local Development Setup

#### Backend Setup
1. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start the backend server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm run dev
```

4. **Open your browser:**
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message and endpoint overview |
| `POST` | `/encrypt` | Encrypt a file (multipart/form-data) |
| `POST` | `/api/encrypt` | Alternative encrypt endpoint |
| `POST` | `/decrypt` | Decrypt a file (not yet implemented) |
| `GET` | `/generate-key` | Generate encryption key |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/download/{temp_id}/{filename}` | Download encrypted files |
| `GET` | `/docs` | Swagger UI Documentation |

### Encryption Request Format
```bash
curl -X POST "http://localhost:8000/encrypt" \
  -F "file=@your-file.txt" \
  -F "algorithm=aes256" \
  -F "key=your-encryption-key"
```

## Supported Encryption Algorithms

| Algorithm | Key Size | Type | Description |
|-----------|----------|------|-------------|
| **AES-128** | 128-bit | Symmetric | Advanced Encryption Standard |
| **AES-256** | 256-bit | Symmetric | Advanced Encryption Standard (stronger) |
| **Blowfish** | Variable | Symmetric | Fast block cipher with variable key length |
| **RSA** | 2048-bit+ | Asymmetric | Public-key cryptography |

## Project Structure
```
├── main.py                     # FastAPI backend server
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── test_encryption_simple.py   # Test script
├── .gitignore                  # Git ignore rules
├── Process/                    # Encryption algorithm implementations
│   ├── Symmetric_algo/         # Symmetric encryption algorithms
│   │   ├── Encryption_algo/    # Encryption implementations
│   │   │   ├── aes128.py      # AES-128 encryption
│   │   │   ├── aes256.py      # AES-256 encryption
│   │   │   └── blowfish.py    # Blowfish encryption
│   │   └── Decryption_algo/    # Decryption implementations
│   │       ├── aes128_dec.py  # AES-128 decryption
│   │       ├── aes256_dec.py  # AES-256 decryption
│   │       └── blowfish_dec.py # Blowfish decryption
│   └── Asymmetric_algo/        # Asymmetric encryption algorithms
│       ├── Encryption/         # RSA encryption
│       │   └── rsa/
│       │       └── rsa.py
│       └── Decryption/         # RSA decryption
│           └── rsa/
│               └── rsa_dec.py
└── frontend/                   # React frontend application
    ├── package.json           # Node.js dependencies
    ├── vite.config.js         # Vite configuration with proxy
    ├── index.html             # HTML entry point
    └── src/                   # React source code
        ├── App.jsx            # Main application component
        ├── main.jsx           # React entry point
        └── pages/             # Page components
            ├── EncryptPage.jsx    # File encryption interface
            ├── DecryptPage.jsx    # File decryption interface
            ├── KeyGenPage.jsx     # Key generation interface
            └── HealthPage.jsx     # Health check interface
```

## Dependencies

### Backend Dependencies
- **FastAPI[all]** 0.109.0 - Modern web framework
- **uvicorn** 0.27.0 - ASGI server
- **python-multipart** 0.0.9 - File upload support
- **cryptography** 42.0.2 - Cryptographic operations
- **pydantic** 2.6.1 - Data validation
- **python-jose[cryptography]** 3.3.0 - JWT handling
- **passlib[bcrypt]** 1.7.4 - Password hashing

### Frontend Dependencies
- **React** 18.2.0 - UI framework
- **Material UI** 5.14.0 - Component library
- **Axios** 1.6.0 - HTTP client
- **Vite** 4.4.0 - Build tool and dev server

## Testing
Run the encryption test to verify functionality:
```bash
python test_encryption_simple.py
```

## Docker Configuration
The project includes Docker support with:
- **Multi-stage build** for optimized production images
- **Volume mounts** for development
- **Environment variables** for configuration
- **Port mapping** (8000:8000) for API access

## Security Considerations
- **Strong key generation** using cryptographically secure random number generation
- **Secure file handling** with temporary file cleanup
- **CORS configuration** for controlled frontend access
- **Input validation** for all API endpoints
- **Secure key derivation** using SHA-256 hashing

## Development Notes
- Frontend uses **Vite proxy** to handle API requests during development
- Backend supports **hot reload** with uvicorn's `--reload` flag
- **CORS middleware** configured for development (restrict origins in production)
- **Temporary file management** for secure file processing


## Troubleshooting

### Common Issues
1. **"Encryption failed" error:**
   - Ensure both backend and frontend are running
   - Check that the backend is accessible at `http://localhost:8000`
   - Verify file upload size limits

2. **CORS errors:**
   - Backend includes CORS middleware configuration
   - Frontend proxy is configured in `vite.config.js`

3. **Module not found errors:**
   - Install Python dependencies: `pip install -r requirements.txt`
   - Install Node.js dependencies: `npm install`
   - Use Docker setup for isolated environment

4. **Port conflicts:**
   - Backend runs on port 8000
   - Frontend runs on port 5173
   - Ensure these ports are available

5. **Frontend black screen or reload issues:**
   - If you see a black screen on `http://localhost:5173/`, check the browser console for errors.
   - Make sure you do not have invalid React code (e.g., hooks outside components).
   - If you reload and get a 404, ensure your Vite config and deployment support client-side routing (see Vite docs for SPA fallback).
   - For production, use a proper static file server or configure your backend to serve the frontend's `index.html` for unknown routes.

6. **File download 404 or not found:**
   - Ensure the backend is returning a valid download URL and the file exists on the server.
   - The frontend should use the backend's `/download/...` endpoint, not try to serve files directly.

7. **Deprecation warnings (Node.js):**
   - These are usually safe to ignore for development, but keep dependencies up to date.

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is open source. Please specify your license terms.

## Disclaimer
This project is designed for educational and development purposes. Always follow security best practices and conduct thorough testing before using in production environments. Ensure proper key management and secure storage of sensitive data.