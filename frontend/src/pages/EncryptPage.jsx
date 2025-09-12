import React, { useState } from 'react';
import { Box, Typography, Paper, TextField, Button, MenuItem, InputLabel, Select, FormControl, LinearProgress, Alert } from '@mui/material';
import axios from 'axios';

const algorithms = [
  { value: 'aes256', label: 'AES-256' },
  { value: 'aes128', label: 'AES-128' },
  { value: 'blowfish', label: 'Blowfish' },
  { value: 'rsa', label: 'RSA' },
];

const backendUrl = "http://localhost:8000";

function EncryptPage() {
  const [file, setFile] = useState(null);
  const [algorithm, setAlgorithm] = useState('aes256');
  const [key, setKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('algorithm', algorithm);
      formData.append('key', key);
      // You may need to adjust the API endpoint and payload as per your backend
      const response = await axios.post('/api/encrypt', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Encryption failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>Encrypt a File</Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <FormControl fullWidth>
          <InputLabel>Algorithm</InputLabel>
          <Select value={algorithm} label="Algorithm" onChange={e => setAlgorithm(e.target.value)}>
            {algorithms.map(a => <MenuItem key={a.value} value={a.value}>{a.label}</MenuItem>)}
          </Select>
        </FormControl>
        <TextField label="Encryption Key" value={key} onChange={e => setKey(e.target.value)} required type="password" />
        <Button variant="contained" component="label">
          Choose File
          <input type="file" hidden onChange={e => setFile(e.target.files[0])} />
        </Button>
        {file && <Typography variant="body2">Selected: {file.name}</Typography>}
        <Button type="submit" variant="contained" disabled={loading || !file || !key}>Encrypt</Button>
        {loading && <LinearProgress />}
        {result && (
          <Alert severity="success">
            Encrypted successfully!
            <a
              href={`http://localhost:8000${result.encrypted_file}`}
              target="_blank"
              rel="noopener noreferrer"
              style={{ marginLeft: '10px', textDecoration: 'underline' }}
            >
              Download {result.original_file}.enc
            </a>
          </Alert>
        )}
        {error && <Alert severity="error">{error}</Alert>}
      </Box>
    </Paper>
  );
}

export default EncryptPage;
