const { z } = require('zod');
const bcrypt = require('bcrypt');
const path = require('path');
const { getByTokenUserModel, getPassword, checkEmail, updateUserModel, updateImageModel, updatePasswordModel } = require('../models/userModel');
const bucket = require('../services/googleCloud');
const userValidate = require('../validation/userSchema')
const passwordValidate = require('../validation/passwordSchema');
const upload = require('../middleware/upload');

const getByTokenUser = async (req, res) => {
    const user_id = req.user_id
    try {
        const data = await getByTokenUserModel(user_id);
        
        if (!data) {
            res.status(404).json({ message: "Data not found" });
        } else {
            res.status(200).json({ message: "Success grab data user", data: data });
        }
    } catch (error) {
        res.status(500).json({ message: "Internal server error" });
    }
};

const updateUser = async (req, res) => {
    const user_id = req.user_id;
    try {
        const { name, email } = userValidate.parse(req.body);

        const updatedUser = await updateUserModel(user_id, name, email);
        
        const { password, ...responseData } = updatedUser;

        res.status(200).json({ message: "User updated successfully", data: responseData });

    } catch (error) {
        if (error instanceof z.ZodError) {
            const errors = error.errors.map((err) => err.message);
            return res.status(400).json({ message: "Validation failed", errors });
        }
        res.status(500).json({ message: "Internal server error" });
    }
};

const updateProfileImage = async (req, res) => {
  const user_id = req.user_id;

  upload.single('profileImage')(req, res, async (err) => {
      if (err) {
          return res.status(400).json({ message: err.message });
      }

      if (!req.file) {
          return res.status(400).json({ message: "No file uploaded" });
      }

      try {
          const fileName = `${user_id}-${Date.now()}${path.extname(req.file.originalname)}`;
          
          const file = bucket.file(fileName);
          const stream = file.createWriteStream({
              resumable: false,
              contentType: req.file.mimetype,
          });

          stream.on('error', (error) => {
              return res.status(500).json({ message: 'Error uploading image', error });
          });

          stream.on('finish', async () => {
              const imageUrl = `https://storage.googleapis.com/${bucket.name}/${fileName}`;

              await updateImageModel(user_id, imageUrl);

              res.status(200).json({ message: 'Profile image updated successfully' });
          });

          stream.end(req.file.buffer);
      } catch (error) {
          console.log(error)
          res.status(500).json({ message: 'Internal Server Error', error });
      }
  });
};

const changePassword = async (req, res) => {
    try {
      const { oldPassword, newPassword, confirmPassword } = passwordValidate.parse(req.body);
      const user_id = req.user_id;
  
      const user = await getPassword(user_id);
  
      if (!user) {
        return res.status(404).json({ message: "User not found" });
      }
  
      const isMatch = await bcrypt.compare(oldPassword, user.password);
  
      if (!isMatch) {
        return res.status(400).json({ message: "Old password is incorrect" });
      }
  
      if (newPassword !== confirmPassword) {
        return res.status(400).json({ message: "New password and confirm password do not match" });
      }
  
      const hashedPassword = await bcrypt.hash(newPassword, 10);
  
      await updatePasswordModel(user_id, hashedPassword);
  
      res.status(200).json({ message: "Password successfully updated" });
  
    } catch (error) {
      if (error instanceof z.ZodError) {
        const errors = error.errors.map((err) => err.message);
        return res.status(400).json({ message: 'Validation failed', errors });
      }
  
      res.status(500).json({ message: "Internal Server Error" });
    }
  };

module.exports = { getByTokenUser, updateUser, updateProfileImage, changePassword };