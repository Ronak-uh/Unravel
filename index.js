const express = require('express');
const path = require('path');

const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Health check endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Unravel Content Automation System',
    status: 'running',
    version: '1.0.0',
    endpoints: {
      pipeline: '/api/pipeline',
      research: '/api/research'
    }
  });
});

// API status endpoint
app.get('/api/status', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// Ghost webhook endpoint (for future use)
app.post('/api/webhook/ghost', (req, res) => {
  console.log('Ghost webhook received:', req.body);
  res.json({ received: true });
});

const PORT = process.env.PORT || 3000;

// For Vercel, export the app
if (process.env.VERCEL) {
  module.exports = app;
} else {
  // For local development
  app.listen(PORT, () => {
    console.log(`Unravel server running on port ${PORT}`);
  });
}