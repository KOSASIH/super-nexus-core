// src/api/v2/middleware/authMiddleware.js

const jwt = require('jsonwebtoken');
const logger = require('../utils/logger'); // Assuming you have a logger utility

// Middleware to authenticate JWT
const authenticateJWT = (req, res, next) => {
    const token = req.header('Authorization')?.split(' ')[1]; // Extract token from Authorization header

    if (!token) {
        logger.warn('No token provided');
        return res.status(401).json({ message: 'Access denied. No token provided.' });
    }

    jwt.verify(token, process.env.JWT_SECRET || 'your_jwt_secret', (err, user) => {
        if (err) {
            logger.warn('Token verification failed', { error: err.message });
            return res.status(403).json({ message: 'Invalid token.' });
        }

        req.user = user; // Attach user information to the request object
        logger.info(`User  authenticated: ${user.username}`);
        next(); // Proceed to the next middleware or route handler
    });
};

// Middleware for role-based access control
const authorizeRoles = (...allowedRoles) => {
    return (req, res, next) => {
        if (!req.user || !allowedRoles.includes(req.user.role)) {
            logger.warn(`Unauthorized access attempt by user: ${req.user?.username}`);
            return res.status(403).json({ message: 'Access denied. You do not have permission to perform this action.' });
        }
        next(); // Proceed to the next middleware or route handler
    };
};

// Export the middleware functions
module.exports = {
    authenticateJWT,
    authorizeRoles,
};
