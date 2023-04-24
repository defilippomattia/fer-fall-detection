# Use an official Golang runtime as a parent image
FROM golang:1.17-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install necessary dependencies
RUN apk add --no-cache git
RUN go mod download

# Build the Go app
RUN go build -o main .

# Expose port 6500 for the container
EXPOSE 6500

# Set environment variables
ENV FFD_MONGO_HOST mongo
ENV FFD_MONGO_PORT 27017
ENV FFD_MONGO_USER root
ENV FFD_MONGO_PASSWORD root
ENV FFD_REDIS_HOST redis
ENV FFD_REDIS_PORT 6379

# Run the Go app when the container starts
CMD ["./main"]
