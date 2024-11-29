const logRequest = (req, res, next) => {
  console.log("logs occurred request to:", req.method, req.path);
  next();
};

module.exports = logRequest;
