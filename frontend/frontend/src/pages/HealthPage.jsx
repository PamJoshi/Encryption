import React, { useState } from 'react';
import { Box, Typography, Paper, Button, LinearProgress, Alert } from '@mui/material';
import axios from 'axios';

function HealthPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const checkHealth = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const response = await axios.get('/api/health');
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Health check failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>API Health Check</Typography>
      <Button variant="contained" onClick={checkHealth} disabled={loading}>Check Health</Button>
      {loading && <LinearProgress sx={{ mt: 2 }} />}
      {result && <Alert severity="success">{result.status}: {result.message}</Alert>}
      {error && <Alert severity="error">{error}</Alert>}
    </Paper>
  );
}

export default HealthPage;
