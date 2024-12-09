const prisma = require("../config/db");

const getByTokenUserModel = async (user_id) => {
  return await prisma.user.findUnique({
    where: {
      id: user_id,
    },
    select: {
      name: true,
      email: true,
      image: true,
    },
  });
};

const getPassword = async (user_id) => {
  return await prisma.user.findUnique({
    where: {
      id: user_id,
    },
    select: {
      password: true,
    },
  });
};

const updateUserModel = async (user_id, name, email) => {
  return await prisma.user.update({
    where: {
      id: user_id,
    },
    data: {
      name: name,
      email: email,
    },
  });
};

const updateImageModel = async (user_id, imageUrl) => {
  return await prisma.user.update({
    where: {
      id: user_id,
    },
    data: {
      image: imageUrl,
    },
  });
};

const updatePasswordModel = async (user_id, hashedPassword) => {
  return await prisma.user.update({
    where: {
      id: user_id,
    },
    data: {
      password: hashedPassword,
    },
  });
};

module.exports = { getByTokenUserModel, getPassword, updateUserModel, updateImageModel, updatePasswordModel };
