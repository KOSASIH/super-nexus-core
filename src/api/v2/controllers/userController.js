// src/api/v2/controllers/userController.js

const User = require('../models/User'); // Assuming you have a User model
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const Joi = require('joi');
const logger = require('../utils/logger'); // Assuming you have a logger utility

// Validation schema using Joi
const userSchema = Joi.object({
    username: Joi.string().min(3).max(30).required(),
    password: Joi.string().min(6).required(),
    email: Joi.string().email().required(),
});

// Register a new user
const registerUser  = async (req, res) => {
    try {
        // Validate request body
        const { error } = userSchema.validate(req.body);
        if (error) {
            return res.status(400).json({ message: error.details[0].message });
        }

        const { username, password, email } = req.body;

        // Check if user already exists
        const existingUser  = await User.findOne({ email });
        if (existingUser ) {
            return res.status(400).json({ message: 'User  already exists.' });
        }

        // Hash the password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create a new user
        const newUser  = new User({ username, email, password: hashedPassword });
        await newUser .save();

        // Log user registration
        logger.info(`User  registered: ${username}`);

        res.status(201).json({ message: 'User  registered successfully.' });
    } catch (error) {
        logger.error(`Error registering user: ${error.message}`);
        res.status(500).json({ message: 'Internal server error.' });
    }
};

// User login
const loginUser  = async (req, res) => {
    try {
        const { email, password } = req.body;

        // Validate request body
        const { error } = Joi.object({
            email: Joi.string().email().required(),
            password: Joi.string().min(6).required(),
        }).validate(req.body);
        if (error) {
            return res.status(400).json({ message: error.details[0].message });
        }

        // Find user by email
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).json({ message: 'Invalid email or password.' });
        }

        // Check password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ message: 'Invalid email or password.' });
        }

        // Generate JWT
        const token = jwt.sign({ id: user._id, username: user.username }, process.env.JWT_SECRET || 'your_jwt_secret', { expiresIn: '1h' });

        // Log user login
        logger.info(`User  logged in: ${user.username}`);

        res.status(200).json({ token });
    } catch (error) {
        logger.error(`Error logging in user: ${error.message}`);
        res.status(500).json({ message: 'Internal server error.' });
    }
};

// Export the controller functions
module.exports = {
    registerUser ,
    loginUser ,
};
