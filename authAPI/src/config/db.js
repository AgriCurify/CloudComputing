const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function checkConnection() {
  try {
    await prisma.$connect();
    console.log("Database connection successful!");
  } catch (error) {
    console.error("Failed to connect to the database:", error);
  }
}

checkConnection();

module.exports = prisma;