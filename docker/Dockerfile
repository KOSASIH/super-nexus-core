# Dockerfile - Dockerfile for building the blockchain application image

# Use the official Node.js image as the base image
FROM node:14

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install application dependencies
RUN npm install --production

# Copy the rest of the application files to the working directory
COPY . .

# Build the application (if applicable)
RUN npm run build

# Expose the application port
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]
