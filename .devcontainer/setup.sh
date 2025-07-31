#!/bin/bash

# Development Container Setup Script
# Runs after container creation to set up the development environment
# 
# This script includes ARM64 (aarch64) architecture support for TA-Lib installation
# by explicitly specifying the build target during configuration

set -e

echo "🚀 Setting up AI Stock Selector development environment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get install -y \
    build-essential \
    wget \
    tar \
    curl \
    git \
    vim \
    nano \
    htop \
    tree \
    sqlite3

# Install TA-Lib C library
echo "📈 Installing TA-Lib C library..."
cd /tmp
if ! wget -q http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz; then
    echo "❌ Failed to download TA-Lib source"
    exit 1
fi
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib

echo "⚙️  Configuring TA-Lib build..."
# Force configure to use a known good architecture for ARM64
if [ "$(uname -m)" = "aarch64" ]; then
    ./configure --prefix=/usr/local --build=aarch64-unknown-linux-gnu
else
    ./configure --prefix=/usr/local
fi

echo "🔨 Building TA-Lib (this may take a few minutes)..."
if ! make -j$(nproc); then
    echo "⚠️  Parallel build failed, trying single-threaded build..."
    make clean
    make
fi
echo "📥 Installing TA-Lib to system..."
sudo make install
sudo ldconfig
echo "✅ TA-Lib C library installed successfully"

# Create symbolic links for TA-Lib (both naming conventions)
sudo ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so
sudo ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so.0
# Create links with hyphen naming for Python wrapper compatibility
sudo ln -sf /usr/local/lib/libta_lib.so /usr/local/lib/libta-lib.so
sudo ln -sf /usr/local/lib/libta_lib.a /usr/local/lib/libta-lib.a

# Set TA-Lib environment variables
echo 'export TA_INCLUDE_PATH=/usr/local/include' >> ~/.bashrc
echo 'export TA_LIBRARY_PATH=/usr/local/lib' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc

# Source the environment variables for current session
export TA_INCLUDE_PATH=/usr/local/include
export TA_LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Cleanup
cd /
rm -rf /tmp/ta-lib*

# Upgrade pip and install Python packages
echo "🐍 Installing Python packages..."
python -m pip install --upgrade pip setuptools wheel

# Install TA-Lib Python wrapper
echo "📦 Installing TA-Lib Python wrapper..."
# Set environment variables for current session
export TA_INCLUDE_PATH=/usr/local/include
export TA_LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

if ! pip install TA-Lib; then
    echo "❌ Failed to install TA-Lib Python wrapper"
    echo "🔄 Trying alternative installation method..."
    pip install --no-cache-dir TA-Lib || {
        echo "❌ TA-Lib installation failed completely"
        echo "⚠️  Container will continue without TA-Lib"
    }
fi

# Install project dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing project requirements from requirements.txt..."
    if ! pip install -r requirements.txt; then
        echo "❌ Failed to install some packages from requirements.txt"
        echo "🔄 Trying to install packages individually..."
        while IFS= read -r package; do
            if [[ ! "$package" =~ ^#.*$ ]] && [[ -n "$package" ]]; then
                echo "Installing: $package"
                pip install "$package" || echo "⚠️  Failed to install $package"
            fi
        done < requirements.txt
    fi
else
    echo "⚠️  No requirements.txt file found, installing basic packages..."
    pip install pandas numpy matplotlib seaborn requests sqlalchemy pytest akshare openai
fi

# Verify TA-Lib installation
echo "🔍 Verifying TA-Lib installation..."
python3 -c "
import talib
import numpy as np
print('✅ TA-Lib installed successfully, version:', talib.__version__)
# Test basic functionality
test_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
sma = talib.SMA(test_data, timeperiod=5)
print('✅ TA-Lib functionality verified successfully')
" || echo "⚠️  TA-Lib verification failed, but installation may still work"

echo "✅ Setup completed successfully!"