# AI Stock Selector - Enhanced Fork with TA-Lib Support

This enhanced fork provides comprehensive TA-Lib installation solutions and a complete development environment for stock analysis and selection using artificial intelligence.

## 🚀 Quick Start

### Option 1: Using Development Container (Recommended)
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Ai_Stock_Selector.git
cd Ai_Stock_Selector

# Open in VS Code with Dev Container
code .
# VS Code will prompt to reopen in container - click "Reopen in Container"
```

### Option 2: Using Docker Compose
```bash
git clone https://github.com/YOUR_USERNAME/Ai_Stock_Selector.git
cd Ai_Stock_Selector

# Start the main application
docker-compose up -d ai-stock-selector

# Or start with Jupyter Lab
docker-compose --profile jupyter up -d

# Access Jupyter Lab at http://localhost:8889
```

### Option 3: Local Installation with Automated Script
```bash
git clone https://github.com/YOUR_USERNAME/Ai_Stock_Selector.git
cd Ai_Stock_Selector

# Run automated TA-Lib installation
./install_talib.sh

# Install Python dependencies
pip install -r requirements.txt

# Generate your first report
python run_enhanced_reports.py
```

## 📋 Features

### Enhanced TA-Lib Support
- ✅ **Automated Installation**: One-click TA-Lib setup script
- ✅ **Cross-Platform**: Works on Linux, macOS, and Windows
- ✅ **Development Container**: Pre-configured environment with TA-Lib
- ✅ **Fallback Implementation**: TA-Lib-free alternative for difficult installations

### Advanced Reporting
- 📊 **Multi-Format Reports**: HTML, Text, and CSV outputs
- 📈 **Technical Analysis**: RSI, MACD, Moving Averages, Bollinger Bands, KDJ
- 🎯 **AI-Powered Scoring**: Intelligent stock ranking and recommendations
- 🌐 **Interactive HTML**: Beautiful web-based reports with responsive design

### Stock Analysis Features
- 📊 Real-time data integration with akshare
- 🤖 AI-powered sentiment analysis
- 📈 Quantitative analysis and scoring
- 💡 Investment recommendations
- 🔍 Risk assessment and management

## 🛠️ Installation Methods

### Method 1: Development Container (Zero Setup)

**Prerequisites**: VS Code with Dev Containers extension

1. **Clone and Open**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Ai_Stock_Selector.git
   code Ai_Stock_Selector
   ```

2. **Reopen in Container**: VS Code will detect the dev container configuration and prompt you to reopen in container.

3. **Ready to Use**: Everything is pre-installed including TA-Lib, Python packages, and development tools.

### Method 2: Automated Local Installation

**Prerequisites**: Linux/macOS with bash, or Windows with WSL

1. **Clone Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Ai_Stock_Selector.git
   cd Ai_Stock_Selector
   ```

2. **Run Installation Script**:
   ```bash
   chmod +x install_talib.sh
   ./install_talib.sh
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**:
   ```bash
   python verify_talib.py
   ```

### Method 3: Manual Installation

Follow the detailed guide in [TALIB_INSTALLATION.md](TALIB_INSTALLATION.md) for step-by-step manual installation instructions.

## 🎯 Usage

### Generate Reports
```bash
# Generate comprehensive stock analysis reports
python run_enhanced_reports.py

# View system overview
python system_overview.py

# Create sample data for testing
python create_sample_data.py
```

### Using the Reports
The system generates three types of reports:

1. **HTML Report** (`report/stock_analysis_*.html`):
   - Interactive web interface
   - Visual charts and indicators
   - Professional styling
   - Best viewing experience

2. **Text Report** (`report/stock_analysis_*.txt`):
   - Detailed analysis
   - Technical indicators
   - Investment recommendations
   - Risk assessments

3. **CSV Summary** (`report/stock_summary_*.csv`):
   - Data table format
   - Easy import to Excel
   - Suitable for further analysis

### Development Environment

```bash
# Start Jupyter Lab (in dev container)
start-jupyter

# Format code
black-format

# Run tests
pytest

# Check code quality
check-lint
```

## 📁 Project Structure

```
Ai_Stock_Selector/
├── .devcontainer/          # Development container configuration
│   ├── devcontainer.json   # VS Code dev container settings
│   ├── Dockerfile          # Container image with TA-Lib
│   └── setup.sh           # Container setup script
├── data/                  # Stock data files (CSV)
├── report/               # Generated analysis reports
├── config.py             # Configuration management
├── main.py              # Main application entry
├── simple_report_generator.py  # Enhanced report generator
├── create_sample_data.py # Sample data generator
├── install_talib.sh     # Automated TA-Lib installer
├── run_enhanced_reports.py    # Report generation runner
├── system_overview.py   # Project overview tool
├── verify_talib.py      # TA-Lib verification script
├── docker-compose.yml   # Docker Compose configuration
├── TALIB_INSTALLATION.md # Comprehensive installation guide
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration

### API Keys Setup
Edit `config.py` to add your API keys for enhanced AI analysis:

```python
DEFAULT = {
    "deepseek": {
        "api_key": "your-deepseek-api-key",
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-coder"
    },
    # ... other providers
}
```

### Environment Variables
```bash
# TA-Lib paths (auto-configured by installation script)
export TA_INCLUDE_PATH="/usr/local/include"
export TA_LIBRARY_PATH="/usr/local/lib"
export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
```

## 🐛 Troubleshooting

### TA-Lib Installation Issues

1. **Import Error**: Run `python verify_talib.py` to diagnose
2. **Library Not Found**: Try the installation script: `./install_talib.sh`
3. **Compilation Fails**: Use the development container
4. **Still Having Issues**: Use the TA-Lib-free alternative in `simple_report_generator.py`

### Common Solutions

| Problem | Solution |
|---------|----------|
| TA-Lib import fails | Run `./install_talib.sh` |
| No data files | Run `python create_sample_data.py` |
| Permission denied | Run `chmod +x install_talib.sh` |
| Docker issues | Try `docker-compose down && docker-compose up --build` |

### Getting Help

1. Check [TALIB_INSTALLATION.md](TALIB_INSTALLATION.md) for detailed installation instructions
2. Run `python system_overview.py` to check system status
3. Use the development container for guaranteed working environment
4. Open an issue with your error message and platform details

## 🚢 Docker Support

### Development Container
- **Full TA-Lib Support**: Pre-compiled and configured
- **VS Code Integration**: Seamless development experience
- **All Dependencies**: Python packages, development tools
- **Port Forwarding**: Automatic port mapping for web services

### Docker Compose Services
```bash
# Main application
docker-compose up ai-stock-selector

# With Jupyter Lab
docker-compose --profile jupyter up

# With database (PostgreSQL)
docker-compose --profile database up

# All services
docker-compose --profile jupyter --profile database up
```

## 📊 Sample Output

### Generated Reports
```
📄 Generated Reports:
  📁 stock_analysis_20250730_142303.html (23.6 KB)
  📁 stock_analysis_20250730_142303.txt (20.1 KB)
  📁 stock_summary_20250730_142303.csv (1.0 KB)

🏆 Stock Ranking:
1. 万科A(000002) - Score: 81 - Strong Buy
2. 五粮液(000858) - Score: 81 - Strong Buy
3. 平安银行(000001) - Score: 76 - Buy
4. 浦发银行(600000) - Score: 62 - Hold
5. 招商银行(600036) - Score: 62 - Hold
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Use the development container for consistent environment
4. Run tests and linting before submitting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TA-Lib**: Technical Analysis Library developers
- **akshare**: Chinese stock market data provider
- **Original Project**: Base AI Stock Selector implementation
- **Community**: Contributors and issue reporters

## 🔗 Links

- [TA-Lib Official Site](http://ta-lib.org/)
- [akshare Documentation](https://akshare.readthedocs.io/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/remote/containers)
- [Docker Documentation](https://docs.docker.com/)

---

**Made with ❤️ for the financial analysis community**
