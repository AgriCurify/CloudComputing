const bcrypt = require('bcrypt');
const{ z } = require('zod')
const prisma = require('../config/db');
const registerValidate = require('../validation/registerSchema');

const register = async (req, res) => {
    try{
        const parsedData = registerValidate.parse(req.body);
        const { name, email, password } = parsedData;
        const existingUser = await prisma.user.findUnique({
            where: { email },
        });
        if (existingUser) {
            return res.status(400).json({ message: "Email already registered" });
          }
        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = await prisma.user.create({
            data: {
              name,
              email,
              password: hashedPassword,
            },
          });
        res.status(201).json({
            message: "User created successfully",
        });
    } catch (error) {
        if (error instanceof z.ZodError){
            const errors = error.errors.map(err => err.message);
            return res.status(400).json({ message: "Validation failed", errors })
        }
        res.status(500).json({ message: "Internal server error" });
    }
};

module.exports = { register };