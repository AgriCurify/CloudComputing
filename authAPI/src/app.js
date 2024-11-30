const express = require('express');
const logRequest = require('./middleware/logs');
const authRoute = require('./routes/authRoute');

const app = express();

app.use(express.json());
app.use(logRequest);

app.get("/", (req, res) => {
  res.send("API AgriCurify");
});

app.use(authRoute);

module.exports = app;