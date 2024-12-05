const express = require('express');
const authRoute = require('./routes/authRoute');
const userRoute = require('./routes/userRoute');

const app = express();

app.use(express.json());

app.use((req, res, next) => {
  console.log("Logs occurred request to:", req.method, req.path);
  next();
});

app.use(authRoute);
app.use(userRoute);

module.exports = app;