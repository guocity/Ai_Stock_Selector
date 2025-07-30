# TA-Lib Installation Guide

This guide provides comprehensive instructions for installing TA-Lib (Technical Analysis Library) across different platforms and environments.

## Table of Contents
- [Overview](#overview)
- [Linux Installation](#linux-installation)
- [macOS Installation](#macos-installation)
- [Windows Installation](#windows-installation)
- [Docker/Container Installation](#dockercontainer-installation)
- [Troubleshooting](#troubleshooting)
- [Verification](#verification)

## Overview

TA-Lib is a technical analysis library that requires both:
1. **C Library**: The core TA-Lib C library
2. **Python Wrapper**: The Python binding (`TA-Lib` package)

Common issues arise from missing system dependencies or incorrect library paths.

## Linux Installation

### Ubuntu/Debian Systems

#### Method 1: Automated Script (Recommended)
```bash
# Run our installation script
chmod +x install_talib.sh
./install_talib.sh
```

#### Method 2: Manual Installation
```bash
# Update package manager
sudo apt-get update

# Install build dependencies
sudo apt-get install -y build-essential wget tar python3-dev python3-pip

# Download and compile TA-Lib C library
cd /tmp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/

# Configure and compile
./configure --prefix=/usr/local
make
sudo make install

# Update library cache
sudo ldconfig

# Create symbolic links (if needed)
sudo ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so
sudo ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so.0

# Install Python wrapper
pip install TA-Lib
```

### CentOS/RHEL/Fedora Systems

```bash
# Install dependencies
sudo yum groupinstall -y "Development Tools"
sudo yum install -y wget tar python3-devel python3-pip

# Or for newer versions:
# sudo dnf groupinstall -y "Development Tools"
# sudo dnf install -y wget tar python3-devel python3-pip

# Follow the same download and compile steps as Ubuntu
cd /tmp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr/local
make
sudo make install
sudo ldconfig

# Install Python wrapper
pip install TA-Lib
```

## macOS Installation

### Using Homebrew (Recommended)
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install TA-Lib
brew install ta-lib

# Install Python wrapper
pip install TA-Lib
```

### Manual Installation
```bash
# Install Xcode command line tools
xcode-select --install

# Download and compile
cd /tmp
curl -L http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -o ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr/local
make
sudo make install

# Install Python wrapper
pip install TA-Lib
```

## Windows Installation

### Method 1: Pre-compiled Wheels
```bash
# Download appropriate wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

# Install the downloaded wheel
pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
```

### Method 2: Using conda
```bash
conda install -c conda-forge ta-lib
```

### Method 3: Manual Compilation (Advanced)
1. Download TA-Lib C library from http://ta-lib.org/hdr_dw.html
2. Extract to `C:\ta-lib`
3. Install Visual Studio Build Tools
4. Set environment variables:
   ```
   set INCLUDE=C:\ta-lib\c\include;%INCLUDE%
   set LIB=C:\ta-lib\c\lib;%LIB%
   ```
5. Install Python wrapper: `pip install TA-Lib`

## Docker/Container Installation

### Dockerfile Example
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Install TA-Lib C library
RUN cd /tmp && \
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    ldconfig && \
    cd / && \
    rm -rf /tmp/ta-lib*

# Install Python wrapper
RUN pip install TA-Lib

# Verify installation
RUN python -c "import talib; print('TA-Lib installed successfully')"
```

## Troubleshooting

### Common Error Messages and Solutions

#### 1. "talib/_ta_lib.c:611:10: fatal error: ta-lib/ta_defs.h: No such file or directory"
**Solution**: C library not installed or not found
```bash
# Reinstall C library
sudo apt-get install build-essential
# Follow Linux installation steps above
```

#### 2. "ImportError: libta_lib.so.0: cannot open shared object file"
**Solution**: Library path issue
```bash
# Update library cache
sudo ldconfig

# Add library path
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
```

#### 3. "Microsoft Visual C++ 14.0 is required" (Windows)
**Solution**: Install Visual Studio Build Tools
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or use pre-compiled wheels

#### 4. "error: Failed building wheel for TA-Lib"
**Solutions**:
```bash
# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Install with verbose output to see specific error
pip install TA-Lib --verbose

# Use conda instead
conda install -c conda-forge ta-lib
```

### Environment Variables (Linux/macOS)
```bash
# Add to ~/.bashrc or ~/.zshrc
export TA_INCLUDE_PATH="/usr/local/include"
export TA_LIBRARY_PATH="/usr/local/lib"
export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
```

### Alternative: TA-Lib-Free Implementation
If TA-Lib installation continues to fail, you can use our simplified technical analysis implementation in `simple_report_generator.py` which doesn't require TA-Lib.

## Verification

### Test Installation
```python
#!/usr/bin/env python3
"""Test TA-Lib installation"""

def test_talib():
    try:
        import talib
        import numpy as np
        
        # Test basic functionality
        close_prices = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        sma = talib.SMA(close_prices, timeperiod=5)
        
        print("✅ TA-Lib installed successfully!")
        print(f"Test SMA calculation: {sma}")
        print(f"TA-Lib version: {talib.__version__}")
        
        # Test more indicators
        rsi = talib.RSI(close_prices, timeperiod=14)
        macd, macdsignal, macdhist = talib.MACD(close_prices)
        
        print("✅ All basic indicators working!")
        return True
        
    except ImportError as e:
        print(f"❌ TA-Lib import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ TA-Lib test failed: {e}")
        return False

if __name__ == "__main__":
    test_talib()
```

Save this as `test_talib.py` and run:
```bash
python test_talib.py
```

## Platform-Specific Notes

### Ubuntu 20.04+
- Default Python 3.8+ works well
- May need `python3-distutils`: `sudo apt-get install python3-distutils`

### Alpine Linux (Docker)
```dockerfile
RUN apk add --no-cache build-base wget tar
# Then follow standard compilation steps
```

### Amazon Linux
```bash
sudo yum install gcc gcc-c++ make wget tar python3-devel
# Then follow standard compilation steps
```

## Getting Help

1. Check our automated installation script: `./install_talib.sh`
2. Use the dev container: `.devcontainer/devcontainer.json`
3. Try the TA-Lib-free alternative in `simple_report_generator.py`
4. Open an issue in the repository with your error message and platform details

## References

- Official TA-Lib: http://ta-lib.org/
- Python wrapper: https://github.com/mrjbq7/ta-lib
- Pre-compiled Windows wheels: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
