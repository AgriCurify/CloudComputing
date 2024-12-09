const prisma = require('../config/db');

const registrationAuthModel = async (name, email, hashedPassword) => {
  return prisma.user.create({
    data: {
      name,
      email,
      password: hashedPassword,
      image: 'https://i.imgur.com/HFmWnmJ.png',
    },
  });
};

const loginAuthModel = async (email) => {
  return prisma.user.findUnique({
    where: { email },
  });
};

const logoutAuthModel = async (token) => {
  return prisma.blacklist.create({
    data: {
      token,
    },
  });
};

const tokenBlacklisted = async (token) => {
  return prisma.blacklist.findUnique({
    where: { token },
  });
};

module.exports = { registrationAuthModel, loginAuthModel, logoutAuthModel, tokenBlacklisted };
