const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();

// Set up multer for file storage
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, path.join(__dirname, 'recordings'));
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

app.post('/save-audio', upload.single('audioFile'), (req, res) => {
    if (req.file) {
        res.json({ message: 'Audio saved successfully' });
    } else {
        res.status(400).json({ message: 'Error saving audio' });
    }
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
