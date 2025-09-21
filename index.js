const Ghost = require('ghost');
const path = require('path');

let ghost;

module.exports = async (req, res) => {
  if (!ghost) {
    try {
      // Initialize Ghost
      ghost = new Ghost({
        url: process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : 'http://localhost:2368',
        admin: {
          url: process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : 'http://localhost:2368'
        },
        database: {
          client: 'sqlite3',
          connection: {
            filename: '/tmp/ghost.db'
          }
        },
        mail: {
          transport: 'Direct'
        },
        logging: {
          transports: ['stdout']
        },
        paths: {
          contentPath: '/tmp/ghost-content'
        },
        privacy: {
          useUpdateCheck: false
        },
        useMinFiles: false,
        caching: {
          frontend: {
            maxAge: 0
          }
        }
      });

      await ghost.start();
    } catch (error) {
      console.error('Failed to start Ghost:', error);
      return res.status(500).json({ error: 'Failed to initialize Ghost' });
    }
  }

  // Handle the request
  try {
    const ghostApp = ghost.rootApp;
    ghostApp(req, res);
  } catch (error) {
    console.error('Ghost request error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};