#!/bin/bash

# Development Container Setup Script
# Runs after container creation to set up the development environment

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
wget -q http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig

# Create symbolic links for TA-Lib
sudo ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so
sudo ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so.0

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
pip install TA-Lib

# Create necessary directories
mkdir -p data report logs .cache

# Set permissions
chmod 755 data report logs

# Install project dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing project requirements..."
    pip install -r requirements.txt
fi

if [ -f "requirements_enhanced.txt" ]; then
    echo "📦 Installing enhanced requirements..."
    pip install -r requirements_enhanced.txt
fi

# Create verification script
echo "🔧 Creating TA-Lib verification script..."
cat > /usr/local/bin/verify-talib << 'EOF'
#!/usr/bin/env python3
# Verify TA-Lib installation in container
try:
    import talib
    import numpy as np
    
    # Test data
    test_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
    
    # Test indicators
    sma = talib.SMA(test_data, timeperiod=5)
    rsi = talib.RSI(test_data, timeperiod=14)
    macd, signal, hist = talib.MACD(test_data)
    
    print("✅ TA-Lib is working correctly in the container!")
    print(f"✅ Version: {talib.__version__}")
    print("✅ All basic indicators tested successfully")
    
except Exception as e:
    print(f"❌ TA-Lib verification failed: {e}")
    exit(1)
EOF

sudo chmod +x /usr/local/bin/verify-talib

# Verify TA-Lib installation
echo "🔍 Verifying TA-Lib installation..."
if command -v verify-talib &> /dev/null; then
    verify-talib
else
    python3 -c "import talib; print('✅ TA-Lib installed successfully, version:', talib.__version__)"
fi

# Initialize sample data if needed
if [ ! -d "data" ] || [ -z "$(ls -A data)" ]; then
    echo "📊 Creating sample data..."
    if [ -f "create_sample_data.py" ]; then
        python3 create_sample_data.py
    fi
fi

# Make scripts executable
echo "🔧 Setting up scripts..."
find . -name "*.sh" -type f -exec chmod +x {} \;
if [ -f "install_talib.sh" ]; then
    chmod +x install_talib.sh
fi

# Set up git hooks (if .git exists)
if [ -d ".git" ]; then
    echo "🔗 Setting up git hooks..."
    if command -v pre-commit &> /dev/null; then
        pre-commit install || echo "⚠️  Pre-commit setup failed, continuing..."
    fi
fi

# Create useful aliases
echo "⚡ Setting up aliases..."
cat >> ~/.bashrc << 'EOF'

# AI Stock Selector aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Project specific aliases
alias run-reports='python3 run_enhanced_reports.py'
alias create-data='python3 create_sample_data.py'
alias verify-talib='python3 -c "import talib; print(\"TA-Lib version:\", talib.__version__)"'
alias start-jupyter='jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root'
alias system-overview='python3 system_overview.py'

# Quick project navigation
alias goto-data='cd data'
alias goto-reports='cd report'
alias goto-root='cd /workspace'

# Development helpers
alias python='python3'
alias pip='pip3'
alias pytest='python3 -m pytest'
alias black-format='black .'
alias check-lint='flake8 .'

echo "🎯 AI Stock Selector Development Environment Ready!"
echo "Type 'run-reports' to generate analysis reports"
echo "Type 'system-overview' to see project status"
EOF

# Source the new aliases
source ~/.bashrc

# Display welcome message
cat << 'EOF'

🎉 Development environment setup completed!

📋 Available commands:
  • run-reports          - Generate comprehensive stock reports
  • create-data          - Create sample stock data
  • system-overview      - Show project overview
  • verify-talib         - Verify TA-Lib installation
  • start-jupyter        - Start Jupyter Lab server

📁 Project structure:
  • data/               - Stock data files (CSV)
  • report/             - Generated analysis reports
  • .devcontainer/      - Container configuration
  • TALIB_INSTALLATION.md - TA-Lib installation guide

🔧 Development tools ready:
  • TA-Lib             - Technical analysis library
  • Python 3.11        - Latest Python runtime
  • Jupyter Lab        - Interactive development
  • Black              - Code formatting
  • Pylint             - Code linting
  • Git                - Version control

Happy coding! 🚀

EOF

echo "✅ Setup completed successfully!"
