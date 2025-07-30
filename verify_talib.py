#!/usr/bin/env python3
"""
TA-Lib Installation Verification Script
Run this script to verify that TA-Lib is properly installed and working.

Usage: python verify_talib.py
"""

import sys
import platform
import subprocess

def print_header():
    """Print verification header"""
    print("🔍 TA-Lib Installation Verification")
    print("=" * 50)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 50)

def check_system_dependencies():
    """Check if system-level TA-Lib is installed"""
    print("\n📋 Checking System Dependencies...")
    
    # Check for TA-Lib library files
    import os
    lib_paths = [
        "/usr/local/lib/libta_lib.so",
        "/usr/local/lib/libta_lib.so.0",
        "/usr/local/lib/libta_lib.so.0.0.0",
        "/usr/lib/libta_lib.so",
        "/opt/homebrew/lib/libta_lib.dylib",  # macOS Homebrew
        "/usr/local/lib/libta_lib.dylib",     # macOS manual install
    ]
    
    found_libs = []
    for lib_path in lib_paths:
        if os.path.exists(lib_path):
            found_libs.append(lib_path)
    
    if found_libs:
        print("✅ TA-Lib C library found:")
        for lib in found_libs:
            print(f"   📁 {lib}")
    else:
        print("❌ TA-Lib C library not found in standard locations")
        print("   Run: ./install_talib.sh to install")
    
    # Check for header files
    header_paths = [
        "/usr/local/include/ta-lib/ta_defs.h",
        "/usr/include/ta-lib/ta_defs.h",
        "/opt/homebrew/include/ta-lib/ta_defs.h",
    ]
    
    found_headers = []
    for header_path in header_paths:
        if os.path.exists(header_path):
            found_headers.append(header_path)
    
    if found_headers:
        print("✅ TA-Lib headers found:")
        for header in found_headers:
            print(f"   📁 {header}")
    else:
        print("❌ TA-Lib headers not found")

def test_talib_import():
    """Test TA-Lib Python package import"""
    print("\n🐍 Testing Python Package Import...")
    
    try:
        import talib
        print("✅ TA-Lib imported successfully")
        print(f"✅ Version: {talib.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import TA-Lib: {e}")
        print("   Solutions:")
        print("   1. Run: pip install TA-Lib")
        print("   2. Run: ./install_talib.sh")
        print("   3. Use development container")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing TA-Lib: {e}")
        return False

def test_basic_functionality():
    """Test basic TA-Lib functionality"""
    print("\n⚙️  Testing Basic Functionality...")
    
    try:
        import talib
        import numpy as np
        
        # Create test data
        test_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        
        # Test SMA
        sma = talib.SMA(test_data, timeperiod=5)
        print("✅ SMA calculation works")
        
        # Test RSI
        rsi_data = np.random.random(100) * 100 + 50
        rsi = talib.RSI(rsi_data, timeperiod=14)
        print("✅ RSI calculation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_advanced_indicators():
    """Test advanced TA-Lib indicators"""
    print("\n🔬 Testing Advanced Indicators...")
    
    try:
        import talib
        import numpy as np
        
        # Generate more realistic test data
        np.random.seed(42)
        high = np.random.random(100) * 10 + 100
        low = high - np.random.random(100) * 5
        close = low + np.random.random(100) * (high - low)
        volume = np.random.randint(1000, 10000, 100).astype(float)
        
        indicators = [
            ("EMA", lambda: talib.EMA(close, timeperiod=20)),
            ("MACD", lambda: talib.MACD(close)),
            ("BBANDS", lambda: talib.BBANDS(close)),
            ("STOCH", lambda: talib.STOCH(high, low, close)),
            ("ADX", lambda: talib.ADX(high, low, close)),
            ("OBV", lambda: talib.OBV(close, volume)),
        ]
        
        for name, func in indicators:
            try:
                result = func()
                print(f"✅ {name} indicator working")
            except Exception as e:
                print(f"❌ {name} indicator failed: {e}")
                return False
        
        print("✅ All advanced indicators working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Advanced indicators test failed: {e}")
        return False

def check_environment():
    """Check environment variables"""
    print("\n🌍 Checking Environment Variables...")
    
    import os
    
    env_vars = [
        "TA_INCLUDE_PATH",
        "TA_LIBRARY_PATH", 
        "LD_LIBRARY_PATH"
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Not set")

def provide_recommendations():
    """Provide recommendations based on test results"""
    print("\n💡 Recommendations:")
    print("-" * 30)
    
    print("✅ If all tests passed:")
    print("   • TA-Lib is working correctly!")
    print("   • Run: python run_enhanced_reports.py")
    print("   • Start developing your stock analysis!")
    
    print("\n❌ If tests failed:")
    print("   • Run: ./install_talib.sh (automated installation)")
    print("   • Use development container (guaranteed working environment)")
    print("   • Check TALIB_INSTALLATION.md for manual installation")
    print("   • Use TA-Lib-free alternative in simple_report_generator.py")
    
    print("\n🐳 Alternative Solutions:")
    print("   • Development Container: code . (reopen in container)")
    print("   • Docker Compose: docker-compose up ai-stock-selector")
    print("   • TA-Lib-free mode: Uses simplified technical analysis")

def main():
    """Main verification function"""
    print_header()
    
    # Run all tests
    tests = [
        ("System Dependencies", check_system_dependencies),
        ("Python Import", test_talib_import),
        ("Basic Functionality", test_basic_functionality),
        ("Advanced Indicators", test_advanced_indicators),
        ("Environment Check", check_environment),
    ]
    
    passed_tests = 0
    total_tests = len(tests) - 1  # Environment check doesn't count as pass/fail
    
    for test_name, test_func in tests:
        try:
            if test_name == "Environment Check":
                test_func()
            else:
                if test_func():
                    passed_tests += 1
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ TA-Lib is fully functional and ready to use")
        success = True
    elif passed_tests > 0:
        print(f"⚠️  PARTIAL SUCCESS: {passed_tests}/{total_tests} tests passed")
        print("🔧 Some functionality may be limited")
        success = False
    else:
        print("❌ ALL TESTS FAILED")
        print("🚨 TA-Lib is not properly installed")
        success = False
    
    provide_recommendations()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
