const { tokenBlacklisted } = require('../models/authModel');
const { verifyToken } = require("../services/jwtService");

const auth = async (req, res, next) => {
  try {
    const authHeaders = req.headers["authorization"];
    if (!authHeaders) {
      return res.status(401).json({ message: "Authentication required" });
    }

    const token = authHeaders.split(" ")[1];
    if (!token) {
      return res.status(401).json({ message: "Token not found" });
    }

    const blacklistEntry = await await tokenBlacklisted(token);

    if (blacklistEntry) {
      return res.status(400).json({
        message: "Your token is blocked. Please log in again."
      });
    }

    const decoded = verifyToken(token);
    req.user_id = decoded.id;
    
    next();
  } catch (err) {
    return res.status(403).json({ message: "Invalid or expired token", error: err.message });
  }
};

module.exports = auth;