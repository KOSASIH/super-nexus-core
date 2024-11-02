// src/api/v1/middleware/authMiddleware.js

const jwt = require('jsonwebtoken');

// Middleware to authenticate users using JWT
const authMiddleware = (req, res, next) => {
    // Get the token from the Authorization header
    const token = req.headers['authorization']?.split(' ')[1]; // Bearer <token>

    if (!token) {
        return res.status(401).json({ message: 'Access denied. No token provided.' });
    }

    try {
        // Verify the token
        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your_jwt_secret');
        req.user = decoded; // Attach the decoded user information to the request object
        next(); // Proceed to the next middleware or route handler
    } catch (error) {
        return res.status(400).json({ message: 'Invalid token.' });
    }
};

module.exports = authMiddleware;
