// src/api/v1/controllers/userController.js

const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');

// In-memory user storage for demonstration (replace with a database in production)
const users = [];

// Constants
const JWT_SECRET = process.env.JWT_SECRET || 'your_jwt_secret'; // Use a strong secret in production

// Helper function to generate JWT
const generateToken = (user) => {
    return jwt.sign({ id: user.id, email: user.email }, JWT_SECRET, { expiresIn: '1h' });
};

// Get all users with pagination
exports.getAllUsers = async (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;

    const resultUsers = users.slice(startIndex, endIndex);
    res.status(200).json({
        total: users.length,
        page: parseInt(page),
        limit: parseInt(limit),
        users: resultUsers,
    });
};

// Create a new user
exports.createUser  = [
    // Validate and sanitize input
    body('name').isString().notEmpty().withMessage('Name is required'),
    body('email').isEmail().withMessage('Valid email is required'),
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),

    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { name, email, password } = req.body;

        // Check if user already exists
        const existingUser  = users.find(user => user.email === email);
        if (existingUser ) {
            return res.status(400).json({ message: 'User  already exists' });
        }

        // Hash the password
        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser  = { id: users.length + 1, name, email, password: hashedPassword };
        users.push(newUser );

        // Generate JWT token
        const token = generateToken(newUser );

        res.status(201).json({ user: { id: newUser .id, name, email }, token });
    }
];

// User login
exports.loginUser  = [
    // Validate input
    body('email').isEmail().withMessage('Valid email is required'),
    body('password').notEmpty().withMessage('Password is required'),

    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { email, password } = req.body;

        // Find user by email
        const user = users.find(user => user.email === email);
        if (!user) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }

        // Check password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }

        // Generate JWT token
        const token = generateToken(user);

        res.status(200).json({ user: { id: user.id, name: user.name, email: user.email }, token });
    }
];
