#!/bin/bash

# Install Google Chrome (Pre-built binary)
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /tmp
dpkg -i /tmp/google-chrome-stable_current_amd64.deb
apt-get install -f  # Automatically install any missing dependencies (without sudo)

# Install ChromeDriver (Pre-built binary)
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
LATEST_DRIVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -N "https://chromedriver.storage.googleapis.com/$LATEST_DRIVER/chromedriver_linux64.zip" -P /tmp
unzip /tmp/chromedriver_linux64.zip -d /tmp
mv /tmp/chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

echo "✅ Google Chrome and ChromeDriver installed successfully!"
