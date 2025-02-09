# Use a lightweight Ubuntu image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    xvfb \
    x11-utils \
    libx11-6 \
    libxtst6 \
    libpng-dev \
    libjpeg-dev \
    libxrandr2 \
    wget \
    unzip

# Set environment variable for PyAutoGUI
ENV DISPLAY=:99

# Install Python libraries
RUN pip3 install flask pyautogui pyperclip gtts

# Copy the Python server script into the container
COPY . /app
WORKDIR /app

# Run Xvfb (virtual screen) and start Flask server
CMD ["bash", "-c", "Xvfb :99 -screen 0 1024x768x16 & python3 main.py"]
