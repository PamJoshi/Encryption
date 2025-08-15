import React from 'react';
import { Container, CssBaseline, Box, Typography, AppBar, Toolbar, Button } from '@mui/material';
import EncryptPage from './pages/EncryptPage';
import DecryptPage from './pages/DecryptPage';
import KeyGenPage from './pages/KeyGenPage';
import HealthPage from './pages/HealthPage';

function App() {
  const [page, setPage] = React.useState('encrypt');

  return (
    <>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Encryption Service
          </Typography>
          <Button color="inherit" onClick={() => setPage('encrypt')}>Encrypt</Button>
          <Button color="inherit" onClick={() => setPage('decrypt')}>Decrypt</Button>
          <Button color="inherit" onClick={() => setPage('keygen')}>Key Gen</Button>
          <Button color="inherit" onClick={() => setPage('health')}>Health</Button>
          <Button color="inherit" href="/docs" target="_blank">API Docs</Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" sx={{ mt: 4 }}>
        {page === 'encrypt' && <EncryptPage />}
        {page === 'decrypt' && <DecryptPage />}
        {page === 'keygen' && <KeyGenPage />}
        {page === 'health' && <HealthPage />}
      </Container>
    </>
  );
}

export default App;
