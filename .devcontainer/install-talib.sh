#!/bin/bash
# Standalone TA-Lib installation script for dev containers

set -e

echo "Installing TA-Lib dependencies..."

# Update package list
sudo apt-get update

# Install build dependencies
sudo apt-get install -y \
    build-essential \
    wget \
    tar \
    curl

# Download and install TA-Lib C library
echo "Downloading TA-Lib source..."
cd /tmp
wget -q http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz

echo "Building TA-Lib..."
cd ta-lib
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig

# Create symbolic links
sudo ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so
sudo ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so.0

echo "Installing Python TA-Lib wrapper..."
export TA_INCLUDE_PATH=/usr/local/include
export TA_LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

pip install TA-Lib

echo "Cleaning up..."
cd /
rm -rf /tmp/ta-lib*

echo "✅ TA-Lib installation completed!"

# Test installation
python3 -c "import talib; print('TA-Lib version:', talib.__version__)"
