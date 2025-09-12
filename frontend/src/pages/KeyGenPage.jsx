import React, { useState } from 'react';
import { Box, Typography, Paper, Button, MenuItem, InputLabel, Select, FormControl, LinearProgress, Alert, TextField } from '@mui/material';
import axios from 'axios';

const algorithms = [
  { value: 'aes256', label: 'AES-256' },
  { value: 'aes128', label: 'AES-128' },
  { value: 'blowfish', label: 'Blowfish' },
  { value: 'rsa', label: 'RSA' },
];

function KeyGenPage() {
  const [algorithm, setAlgorithm] = useState('aes256');
  const [length, setLength] = useState(32);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const response = await axios.get('/api/generate-key', {
        params: { algorithm, length },
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Key generation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>Generate Encryption Key</Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <FormControl fullWidth>
          <InputLabel>Algorithm</InputLabel>
          <Select value={algorithm} label="Algorithm" onChange={e => setAlgorithm(e.target.value)}>
            {algorithms.map(a => <MenuItem key={a.value} value={a.value}>{a.label}</MenuItem>)}
          </Select>
        </FormControl>
        <TextField label="Key Length" type="number" value={length} onChange={e => setLength(e.target.value)} fullWidth />
        <Button type="submit" variant="contained" disabled={loading}>Generate Key</Button>
        {loading && <LinearProgress />}
        {result && <Alert severity="success">Key: <code>{result.key}</code></Alert>}
        {error && <Alert severity="error">{error}</Alert>}
      </Box>
    </Paper>
  );
}

export default KeyGenPage;
