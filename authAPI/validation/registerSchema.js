const { z } = require('zod');

const registerValidate = z.object({
    name: z.string()
        .min(3, { message: "Name must be at least 3 characters long" })
        .max(100, { message: "Name must be at most 100 characters long" }),
    
    email: z.string()
        .email({ message: "Invalid email address" }),
    
    password: z.string()
        .min(8, { message: "Password must be at least 8 characters long" })
        .regex(/^[A-Za-z\d]{8,}$/, { message: "Password must contain only letters and numbers, and be at least 8 characters long"})
});

module.exports = registerValidate;