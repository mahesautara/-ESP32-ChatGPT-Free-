# Use a lightweight Ubuntu image
FROM ubuntu:latest

# Update package list & install system dependencies
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
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    wget \
    unzip \
    curl \
    sudo \
    dbus-x11 \
    fonts-liberation \
    libappindicator3-1 \
    libdbusmenu-glib4 \
    libdbusmenu-gtk3-4 \
    libxdamage1 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    chromium-browser \
    chromium-chromedriver

# Set environment variable for PyAutoGUI
ENV DISPLAY=:99

# Install Python libraries
RUN pip3 install --upgrade pip
RUN pip3 install flask pyautogui pyperclip gtts selenium

# Set up a working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Run Xvfb (virtual screen) and start Flask server
CMD ["bash", "-c", "Xvfb :99 -screen 0 1024x768x16 & python3 main.py"]
