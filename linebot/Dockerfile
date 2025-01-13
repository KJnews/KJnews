# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv wget tar && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Create a virtual environment and install requirements
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Install ngrok
RUN wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz && \
    tar xvzf ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin && \
    rm ngrok-v3-stable-linux-amd64.tgz &&\
    ngrok authtoken <NGROK_AUTHTOKEN>

# Expose the port that the app runs on
EXPOSE 5000

# Run the application and ngrok in the background
CMD ["sh", "-c", ". venv/bin/activate && python app.py & sh ngrok_startup.sh"]