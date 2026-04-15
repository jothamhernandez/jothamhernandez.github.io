# Build stage
FROM node:20-alpine AS build

# Set working directory
WORKDIR /src

# Copy package management files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the Nuxt application
RUN npm run build

# Runtime stage
FROM node:20-alpine AS runtime

# Set working directory
WORKDIR /app

# Copy the build output from the build stage
COPY --from=build /src/.output ./.output

# Expose the application port (default for Nuxt is 3000)
EXPOSE 3000

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=3000
ENV NODE_ENV=production

# Run the application
CMD ["node", ".output/server/index.mjs"]
