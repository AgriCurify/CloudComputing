const bcrypt = require('bcrypt');
const { z } = require('zod');
const { registrationAuthModel, loginAuthModel, logoutAuthModel } = require('../models/authModel');
const registerValidate = require('../validation/registerSchema');
const loginValidate = require('../validation/loginSchema');
const { generateToken } = require('../services/jwtService');

const register = async (req, res) => {
  try {
    const { name, email, password } = registerValidate.parse(req.body);
    const existingUser = await loginAuthModel(email);
    if (existingUser) {
      return res.status(400).json({ message: "Email already registered" });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    await registrationAuthModel(name, email, hashedPassword);

    res.status(201).json({ message: "User created successfully" });
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errors = error.errors.map((err) => err.message);
      return res.status(400).json({ message: "Validation failed", errors });
    }
    res.status(500).json({ message: "Internal server error" });
  }
};

const login = async (req, res) => {
  try {
    const { email, password } = loginValidate.parse(req.body);
    const existingUser = await loginAuthModel(email);

    if (!existingUser) {
      return res.status(400).json({ message: "Invalid email or password" });
    }

    const isPasswordValid = await bcrypt.compare(password, existingUser.password);
    if (!isPasswordValid) {
      return res.status(400).json({ message: "Invalid email or password" });
    }

    const token = generateToken(existingUser);
    res.status(200).json({ message: "Login successful", token });
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errors = error.errors.map((err) => err.message);
      return res.status(400).json({ message: "Validation failed", errors });
    }
    res.status(500).json({ message: "Internal server error" });
  }
};

const logout = async (req, res) => {
  try {
    const token = req.headers.authorization?.split(" ")[1];
    if (!token) {
      return res.status(400).json({ message: "No token provided" });
    }

    await logoutAuthModel(token);
    res.status(200).json({ message: "Logged out successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Internal server error" });
  }
};

module.exports = { register, login, logout };