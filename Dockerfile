# Use a lightweight Ubuntu image
FROM ubuntu:latest

# Update package list & install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
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

# Create a virtual environment for Python
RUN python3 -m venv /app/venv

# Activate the virtual environment & install Python packages
RUN /app/venv/bin/pip install --no-cache-dir flask pyautogui pyperclip gtts selenium

# Set environment variable for PyAutoGUI
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Ensure any previous Xvfb lock is removed before starting
CMD ["bash", "-c", "rm -f /tmp/.X99-lock && Xvfb :99 -screen 0 1024x768x16 & /app/venv/bin/python main.py"]
