const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK, message: 'commerance API is running''})
});

app.listen(port, () => {
  console.log('Server listening on port ${port}')
});
