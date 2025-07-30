#!/usr/bin/env python3
"""
AI Stock Selector - Setup Helper
Provides guidance on setting up the enhanced stock selector with TA-Lib support
"""

import os
import sys
import platform
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("🎯 AI Stock Selector - Enhanced Fork Setup")
    print("=" * 60)
    print("Complete setup guide for TA-Lib and stock analysis")
    print("=" * 60)

def check_current_environment():
    """Check the current environment status"""
    print("\n🔍 Current Environment Status:")
    print("-" * 40)
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"🐍 Python: {python_version}")
    
    # Check platform
    system = platform.system()
    print(f"💻 Platform: {system} {platform.release()}")
    
    # Check if we're in a container
    in_container = Path("/.dockerenv").exists() or os.environ.get("CONTAINER") == "true"
    if in_container:
        print("🐳 Environment: Docker Container")
    else:
        print("🖥️  Environment: Local Machine")
    
    # Check TA-Lib status
    try:
        import talib
        print(f"✅ TA-Lib: Installed (v{talib.__version__})")
        talib_status = "working"
    except ImportError:
        print("❌ TA-Lib: Not installed or not working")
        talib_status = "missing"
    except Exception as e:
        print(f"⚠️  TA-Lib: Installed but has issues ({e})")
        talib_status = "issues"
    
    # Check project files
    important_files = [
        "install_talib.sh",
        "verify_talib.py", 
        "simple_report_generator.py",
        ".devcontainer/devcontainer.json",
        "docker-compose.yml",
        "TALIB_INSTALLATION.md"
    ]
    
    print("\n📁 Project Files:")
    for file in important_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    
    return talib_status, system.lower(), in_container

def recommend_setup_method(talib_status, system, in_container):
    """Recommend the best setup method based on environment"""
    print("\n🚀 Recommended Setup Methods:")
    print("-" * 40)
    
    if talib_status == "working":
        print("🎉 TA-Lib is already working! You can:")
        print("   1. python run_enhanced_reports.py  # Generate reports")
        print("   2. python system_overview.py       # Check system status")
        print("   3. python create_sample_data.py    # Create test data")
        return
    
    if in_container:
        print("🐳 You're in a container. Try:")
        print("   1. Rebuild container: docker-compose up --build")
        print("   2. Use development container with VS Code")
        print("   3. Check container setup with: verify-talib")
    
    # Recommendations by platform
    if system in ["linux", "darwin"]:  # Linux or macOS
        print("🔧 Method 1: Automated Installation (Recommended)")
        print("   ./install_talib.sh")
        print("")
        print("🐳 Method 2: Development Container (Easiest)")
        print("   # In VS Code: Reopen in Container")
        print("   # Or use: docker-compose up ai-stock-selector")
        print("")
        print("📖 Method 3: Manual Installation")
        print("   # Follow guide in TALIB_INSTALLATION.md")
        print("")
        print("🔄 Method 4: TA-Lib-Free Alternative")
        print("   python simple_report_generator.py")
        
    elif system == "windows":
        print("🪟 Windows Setup Options:")
        print("   1. Use WSL + automated script: ./install_talib.sh")
        print("   2. Development container (recommended)")
        print("   3. Pre-compiled wheels from UCI")
        print("   4. conda install -c conda-forge ta-lib")
    
    else:
        print("❓ Unknown platform. Try:")
        print("   1. Development container (safest option)")
        print("   2. TA-Lib-free alternative")

def show_quick_commands():
    """Show quick commands for common tasks"""
    print("\n⚡ Quick Commands:")
    print("-" * 40)
    
    commands = [
        ("🔧 Install TA-Lib", "./install_talib.sh"),
        ("✅ Verify TA-Lib", "python verify_talib.py"),
        ("📊 Generate Reports", "python run_enhanced_reports.py"),
        ("📈 Create Sample Data", "python create_sample_data.py"),
        ("🔍 System Overview", "python system_overview.py"),
        ("🐳 Start Container", "docker-compose up ai-stock-selector"),
        ("📓 Start Jupyter", "docker-compose --profile jupyter up"),
        ("🌐 Simple Reports", "python simple_report_generator.py"),
    ]
    
    for description, command in commands:
        print(f"   {description:20} {command}")

def show_troubleshooting():
    """Show troubleshooting tips"""
    print("\n🛠️  Troubleshooting:")
    print("-" * 40)
    
    issues = [
        ("TA-Lib import fails", [
            "Run: ./install_talib.sh",
            "Try: pip uninstall TA-Lib && pip install TA-Lib", 
            "Use: Development container"
        ]),
        ("Permission denied", [
            "Run: chmod +x install_talib.sh",
            "Use: sudo for system installation",
            "Try: Development container"
        ]),
        ("Compilation errors", [
            "Install: build-essential (Ubuntu) or Xcode (macOS)",
            "Use: Pre-built development container",
            "Try: TA-Lib-free alternative"
        ]),
        ("No data files", [
            "Run: python create_sample_data.py",
            "Check: data/ directory exists",
            "Download: Real stock data with akshare"
        ])
    ]
    
    for issue, solutions in issues:
        print(f"\n❌ {issue}:")
        for solution in solutions:
            print(f"   • {solution}")

def show_next_steps():
    """Show next steps after setup"""
    print("\n🎯 Next Steps After Setup:")
    print("-" * 40)
    
    steps = [
        "1. Verify installation: python verify_talib.py",
        "2. Create sample data: python create_sample_data.py", 
        "3. Generate first report: python run_enhanced_reports.py",
        "4. View HTML report in browser",
        "5. Configure API keys in config.py (optional)",
        "6. Add real stock data sources",
        "7. Customize analysis parameters",
        "8. Set up automated reporting"
    ]
    
    for step in steps:
        print(f"   {step}")

def show_resources():
    """Show helpful resources"""
    print("\n📚 Resources:")
    print("-" * 40)
    
    resources = [
        ("📖 Installation Guide", "TALIB_INSTALLATION.md"),
        ("🐳 Container Config", ".devcontainer/devcontainer.json"),
        ("🔧 Setup Script", "install_talib.sh"),
        ("✅ Verification", "verify_talib.py"),
        ("📊 Report Generator", "simple_report_generator.py"),
        ("🌐 Enhanced README", "README_ENHANCED.md"),
        ("⚙️  Dependencies", "requirements_enhanced.txt"),
    ]
    
    for name, file in resources:
        if Path(file).exists():
            print(f"   ✅ {name:20} {file}")
        else:
            print(f"   ❌ {name:20} {file} (missing)")

def main():
    """Main setup helper function"""
    print_banner()
    
    # Check environment
    talib_status, system, in_container = check_current_environment()
    
    # Provide recommendations
    recommend_setup_method(talib_status, system, in_container)
    
    # Show commands and troubleshooting
    show_quick_commands()
    show_troubleshooting()
    show_next_steps()
    show_resources()
    
    print("\n" + "=" * 60)
    print("🎉 Ready to analyze stocks with AI!")
    print("Need help? Check the documentation or open an issue.")
    print("=" * 60)

if __name__ == "__main__":
    main()
