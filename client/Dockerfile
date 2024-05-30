# Use the official Node.js 14 image as the base image
FROM node:20

# Create and set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (or yarn.lock) to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm install
# If you're using Yarn, use the following line instead:
# RUN yarn install

# Copy the rest of the application code to the working directory
COPY . .

RUN npm run build

# Expose the port the app runs on
EXPOSE 5173

# Define the command to run the app
CMD ["node", "nodeServer/nodeServer.js"]
