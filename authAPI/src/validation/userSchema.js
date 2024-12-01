const { z } = require("zod");

const userValidate = z.object({
  name: z
    .string()
    .min(3, { message: "Name must be at least 3 characters long" })
    .max(100, { message: "Name must be at most 100 characters long" }),

  email: z
    .string()
    .email({ message: "Invalid email address" }),
});

module.exports = userValidate;