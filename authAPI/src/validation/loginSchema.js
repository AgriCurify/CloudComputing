const { z } = require('zod');

const loginValidate = z.object({
  email: z.string().email().nonempty(),
  password: z.string().nonempty(),
});

module.exports = loginValidate;