const { z } = require('zod');

const passwordValidate = z.object({
  oldPassword: z
    .string()
    .min(8, { message: "Password must be at least 8 characters long" })
    .regex(/^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]+$/, { message: "Password must contain letters and numbers only, and be at least 8 characters long" }),

  newPassword: z
    .string()
    .min(8, { message: "Password must be at least 8 characters long" })
    .regex(/^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]+$/, { message: "Password must contain letters and numbers only, and be at least 8 characters long" }),

  confirmPassword: z
    .string()
    .superRefine((val, ctx) => val === ctx.parent?.newPassword, { message: "Passwords do not match" })
});

module.exports = passwordValidate;
