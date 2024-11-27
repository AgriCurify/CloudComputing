const express = require('express');
const dotenv = require('dotenv');
const logRequest = require('./middleware/logs');

dotenv.config();

const app = express();
const PORT = process.env.PORT;

app.use(express.json());
app.use(logRequest);

app.get("/", (req, res) => {
    res.send("API AgriCurify");
});

app.listen(PORT, () => {
    console.log("Server running on http://localhost:" + PORT);
});