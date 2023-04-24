# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt

RUN pip install --trusted-host pypi.python.org redis flask

# Make port 6504 available to the world outside this container
EXPOSE 6504

# Run app.py when the container launches
CMD ["python", "app.py"]
