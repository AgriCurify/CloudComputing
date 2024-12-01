const express = require('express');
const auth = require('../middleware/authentication')
const { getByTokenUser, changePassword, updateUser } = require('../controller/userController');

const router = express.Router();

router.get("/users", auth, getByTokenUser);
router.put("/users", auth, updateUser);
router.put("/users/changePassword", auth, changePassword);


module.exports = router;