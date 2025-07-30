#!/bin/bash

# TA-Lib Installation Script
# Automated installation of TA-Lib C library and Python wrapper
# Supports Ubuntu, Debian, CentOS, RHEL, Fedora, and macOS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root. This script will install system-wide."
        SUDO=""
    else
        SUDO="sudo"
    fi
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
            OS_VERSION=$VERSION_ID
        elif [ -f /etc/redhat-release ]; then
            OS="rhel"
        else
            OS="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    
    log_info "Detected OS: $OS"
}

# Install system dependencies
install_dependencies() {
    log_info "Installing system dependencies..."
    
    case $OS in
        ubuntu|debian)
            $SUDO apt-get update -y
            $SUDO apt-get install -y build-essential wget tar python3-dev python3-pip curl
            if ! command -v python3-distutils &> /dev/null; then
                $SUDO apt-get install -y python3-distutils || true
            fi
            ;;
        centos|rhel|fedora)
            if command -v dnf &> /dev/null; then
                $SUDO dnf groupinstall -y "Development Tools"
                $SUDO dnf install -y wget tar python3-devel python3-pip curl
            else
                $SUDO yum groupinstall -y "Development Tools"
                $SUDO yum install -y wget tar python3-devel python3-pip curl
            fi
            ;;
        macos)
            if ! command -v brew &> /dev/null; then
                log_info "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            
            # Check if Xcode command line tools are installed
            if ! command -v gcc &> /dev/null; then
                log_info "Installing Xcode command line tools..."
                xcode-select --install
                log_warning "Please complete Xcode installation and run this script again."
                exit 1
            fi
            ;;
        *)
            log_error "Unsupported operating system: $OS"
            exit 1
            ;;
    esac
    
    log_success "Dependencies installed successfully"
}

# Download and compile TA-Lib C library
install_talib_c() {
    log_info "Installing TA-Lib C library..."
    
    if [[ "$OS" == "macos" ]] && command -v brew &> /dev/null; then
        # Use Homebrew on macOS
        log_info "Using Homebrew to install TA-Lib..."
        brew install ta-lib
        log_success "TA-Lib C library installed via Homebrew"
        return 0
    fi
    
    # Manual compilation for Linux
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    log_info "Downloading TA-Lib source code..."
    wget -q http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
    
    if [ ! -f ta-lib-0.4.0-src.tar.gz ]; then
        log_error "Failed to download TA-Lib source"
        exit 1
    fi
    
    log_info "Extracting source code..."
    tar -xzf ta-lib-0.4.0-src.tar.gz
    cd ta-lib
    
    log_info "Configuring build..."
    ./configure --prefix=/usr/local
    
    log_info "Compiling (this may take a few minutes)..."
    make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 2)
    
    log_info "Installing..."
    $SUDO make install
    
    # Update library cache on Linux
    if [[ "$OS" != "macos" ]]; then
        $SUDO ldconfig || true
        
        # Create symbolic links if they don't exist
        if [ -f /usr/local/lib/libta_lib.so.0.0.0 ]; then
            $SUDO ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so || true
            $SUDO ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so.0 || true
        fi
    fi
    
    # Cleanup
    cd /
    rm -rf "$temp_dir"
    
    log_success "TA-Lib C library compiled and installed"
}

# Install Python wrapper
install_talib_python() {
    log_info "Installing TA-Lib Python wrapper..."
    
    # Upgrade pip first
    python3 -m pip install --upgrade pip setuptools wheel
    
    # Set environment variables for compilation
    if [[ "$OS" != "macos" ]]; then
        export TA_INCLUDE_PATH="/usr/local/include"
        export TA_LIBRARY_PATH="/usr/local/lib"
        export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
    fi
    
    # Try to install TA-Lib
    if python3 -m pip install TA-Lib; then
        log_success "TA-Lib Python wrapper installed successfully"
    else
        log_warning "Standard installation failed, trying with verbose output..."
        
        # Try with more specific options
        if [[ "$OS" == "macos" ]]; then
            # On macOS, specify Homebrew paths
            export TA_INCLUDE_PATH="$(brew --prefix ta-lib)/include"
            export TA_LIBRARY_PATH="$(brew --prefix ta-lib)/lib"
        fi
        
        python3 -m pip install TA-Lib --verbose
    fi
}

# Test installation
test_installation() {
    log_info "Testing TA-Lib installation..."
    
    cat > /tmp/test_talib.py << 'EOF'
import sys
try:
    import talib
    import numpy as np
    
    # Test basic functionality
    close_prices = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
    sma = talib.SMA(close_prices, timeperiod=5)
    
    print("✅ TA-Lib installed successfully!")
    print(f"✅ TA-Lib version: {talib.__version__}")
    print("✅ Basic SMA calculation works")
    
    # Test additional indicators
    rsi = talib.RSI(close_prices, timeperiod=14)
    macd, macdsignal, macdhist = talib.MACD(close_prices)
    
    print("✅ Advanced indicators working")
    print("🎉 All tests passed!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)
EOF
    
    if python3 /tmp/test_talib.py; then
        log_success "TA-Lib installation test passed!"
        rm -f /tmp/test_talib.py
        return 0
    else
        log_error "TA-Lib installation test failed!"
        rm -f /tmp/test_talib.py
        return 1
    fi
}

# Setup environment variables
setup_environment() {
    log_info "Setting up environment variables..."
    
    local shell_rc=""
    if [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    else
        shell_rc="$HOME/.profile"
    fi
    
    if [[ "$OS" != "macos" ]]; then
        # Add environment variables to shell config
        cat >> "$shell_rc" << 'EOF'

# TA-Lib environment variables
export TA_INCLUDE_PATH="/usr/local/include"
export TA_LIBRARY_PATH="/usr/local/lib"
export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
EOF
        
        log_info "Environment variables added to $shell_rc"
        log_info "Run 'source $shell_rc' or restart your shell to apply changes"
    fi
}

# Install additional Python packages that work well with TA-Lib
install_related_packages() {
    log_info "Installing related packages..."
    
    python3 -m pip install numpy pandas matplotlib seaborn yfinance akshare
    
    log_success "Related packages installed"
}

# Create a verification script
create_verification_script() {
    log_info "Creating verification script..."
    
    cat > verify_talib.py << 'EOF'
#!/usr/bin/env python3
"""
TA-Lib Installation Verification Script
Run this script to verify that TA-Lib is properly installed and working.
"""

def verify_talib():
    """Comprehensive TA-Lib verification"""
    print("🔍 TA-Lib Installation Verification")
    print("=" * 50)
    
    try:
        import talib
        print(f"✅ TA-Lib imported successfully")
        print(f"✅ Version: {talib.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import TA-Lib: {e}")
        return False
    
    try:
        import numpy as np
        
        # Create test data
        test_data = np.random.random(100) * 100 + 50
        
        # Test various indicators
        indicators = [
            ("SMA", lambda: talib.SMA(test_data, timeperiod=20)),
            ("EMA", lambda: talib.EMA(test_data, timeperiod=20)),
            ("RSI", lambda: talib.RSI(test_data, timeperiod=14)),
            ("MACD", lambda: talib.MACD(test_data)),
            ("BBANDS", lambda: talib.BBANDS(test_data)),
            ("STOCHASTIC", lambda: talib.STOCH(test_data, test_data, test_data)),
        ]
        
        for name, func in indicators:
            try:
                result = func()
                print(f"✅ {name} indicator working")
            except Exception as e:
                print(f"❌ {name} indicator failed: {e}")
                return False
        
        print("\n🎉 All TA-Lib indicators are working correctly!")
        print("✅ Installation verification completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    verify_talib()
EOF
    
    chmod +x verify_talib.py
    log_success "Created verify_talib.py script"
}

# Main installation function
main() {
    echo "🎯 TA-Lib Automated Installation Script"
    echo "======================================"
    echo "This script will install TA-Lib C library and Python wrapper"
    echo ""
    
    check_root
    detect_os
    
    # Confirm installation
    echo "Detected OS: $OS"
    echo -n "Proceed with installation? (y/N): "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        log_info "Installation cancelled"
        exit 0
    fi
    
    # Installation steps
    install_dependencies
    install_talib_c
    install_talib_python
    
    # Test installation
    if test_installation; then
        setup_environment
        install_related_packages
        create_verification_script
        
        echo ""
        log_success "🎉 TA-Lib installation completed successfully!"
        echo ""
        echo "Next steps:"
        echo "1. Run 'source ~/.bashrc' (or restart your shell)"
        echo "2. Run 'python3 verify_talib.py' to verify installation"
        echo "3. Start using TA-Lib in your Python projects!"
        echo ""
        echo "Example usage:"
        echo "  import talib"
        echo "  import numpy as np"
        echo "  prices = np.array([1,2,3,4,5], dtype=float)"
        echo "  sma = talib.SMA(prices, timeperiod=3)"
        
    else
        log_error "Installation failed. Please check the error messages above."
        log_info "You can try using our TA-Lib-free alternative in simple_report_generator.py"
        exit 1
    fi
}

# Run main function
main "$@"
