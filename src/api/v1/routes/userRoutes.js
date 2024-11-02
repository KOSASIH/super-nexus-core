// src/api/v1/routes/userRoutes.js

const express = require('express');
const userController = require('../controllers/userController');
const authMiddleware = require('../middleware/authMiddleware');

const router = express.Router();

// Route to get all users (with pagination)
router.get('/', userController.getAllUsers);

// Route to create a new user (registration)
router.post('/', userController.createUser );

// Route to log in a user
router.post('/login', userController.loginUser );

// Optional: Protected route example (requires authentication)
router.get('/me', authMiddleware, (req, res) => {
    // Assuming req.user is set by the authMiddleware
    res.status(200).json({ user: req.user });
});

// Export the router
module.exports = router;
