const express = require('express');
const auth = require('../middleware/authentication')
const { getByTokenUser, updateUser, updateProfileImage, changePassword } = require('../controller/userController');

const router = express.Router();

router.get("/users", auth, getByTokenUser);
router.put("/users", auth, updateUser);
router.put("/users/updateProfile", auth, updateProfileImage);
router.put("/users/changePassword", auth, changePassword);


module.exports = router;