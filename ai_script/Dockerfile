# Use the official Python image from Docker Hub as a base image
FROM python:3.11-slim
RUN pip install --upgrade pip 
RUN apt-get update && apt-get install -y \
curl
RUN mkdir /app

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file from the parent folder to the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh
# Copy the source code into the container
COPY . /app

# Expose the port that Uvicorn will listen on (8050 as per your update)
EXPOSE 8050

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8050", "--reload"]
