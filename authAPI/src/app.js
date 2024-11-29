const express = require("express");
const logRequest = require("./middleware/logs");
const authRoutes = require("./routes/authRoutes");

const app = express();

app.use(express.json());
app.use(logRequest);

app.get("/", (req, res) => {
  res.send("API AgriCurify");
});

app.use(authRoutes);

module.exports = app;