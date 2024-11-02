// src/api/v2/routes/userRoutes.js

const express = require('express');
const { registerUser , loginUser  } = require('../controllers/userController');
const rateLimit = require('express-rate-limit');
const { authenticateJWT } = require('../middleware/authMiddleware'); // Assuming you have JWT authentication middleware
const logger = require('../utils/logger'); // Assuming you have a logger utility

const router = express.Router();

// Rate limiting for registration and login
const registerLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // Limit each IP to 5 registration requests per windowMs
    message: { message: 'Too many registration attempts, please try again later.' }
});

const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 10, // Limit each IP to 10 login requests per windowMs
    message: { message: 'Too many login attempts, please try again later.' }
});

// User registration route
router.post('/register', registerLimiter, (req, res) => {
    logger.info('Registration attempt');
    registerUser (req, res);
});

// User login route
router.post('/login', loginLimiter, (req, res) => {
    logger.info('Login attempt');
    loginUser (req, res);
});

// Protected route example (e.g., get user profile)
router.get('/profile', authenticateJWT, (req, res) => {
    // Assuming you have a function to get user profile
    res.status(200).json({ message: 'User  profile data', user: req.user });
});

// Export the router
module.exports = router;
