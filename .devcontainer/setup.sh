#!/bin/bash

# Development Container Setup Script
# Runs after container creation to set up the development environment

set -e

echo "🚀 Setting up AI Stock Selector development environment..."

# Create necessary directories
mkdir -p data report logs .cache

# Set permissions
chmod 755 data report logs

# Install project dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing project requirements..."
    pip install -r requirements.txt
fi

# Verify TA-Lib installation
echo "🔍 Verifying TA-Lib installation..."
if command -v verify-talib &> /dev/null; then
    verify-talib
else
    python3 -c "import talib; print('✅ TA-Lib installed successfully')"
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
