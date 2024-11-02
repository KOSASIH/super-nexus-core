// src/api/v2/index.js

const express = require('express');
const userRoutes = require('./routes/userRoutes'); // Import user routes for v2
const bodyParser = require('body-parser');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const morgan = require('morgan');
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json'); // Assuming you have a swagger.json file
const config = require('config'); // For environment configuration

const app = express();

// Middleware
app.use(helmet()); // Set security HTTP headers
app.use(cors()); // Enable CORS for all routes
app.use(bodyParser.json()); // Parse JSON request bodies
app.use(morgan('combined')); // Log requests to the console

// Rate Limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: { message: 'Too many requests, please try again later.' }
});
app.use(limiter); // Apply rate limiting to all requests

// API Versioning
app.use('/api/v2/users', userRoutes); // User routes for version 2

// Swagger API Documentation
app.use('/api/v2/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Health check route
app.get('/api/v2/health', (req, res) => {
    res.status(200).json({ message: 'API v2 is running', version: '2.0.0' });
});

// Enhanced Error Handling Middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    const statusCode = err.status || 500;
    res.status(statusCode).json({
        status: 'error',
        statusCode,
        message: err.message || 'Internal Server Error',
        stack: process.env.NODE_ENV === 'development' ? err.stack : undefined // Show stack trace in development
    });
});

// Export the app
module.exports = app;
