const path = require('path');

const express = require('express');

const app = express();
const PORT = 5173;

app.use(express.static(path.join(__dirname, '..', 'dist')));

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
