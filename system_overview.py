#!/usr/bin/env python3
"""
AI Stock Selector - System Overview
Provides an overview of all available features and generated reports
"""

import os
from pathlib import Path
from datetime import datetime
import glob

def show_system_overview():
    print("🎯 AI Stock Selector - System Overview")
    print("=" * 60)
    
    # Check data directory
    data_dir = Path("data")
    if data_dir.exists():
        csv_files = list(data_dir.glob("*.csv"))
        db_files = list(data_dir.glob("*.db"))
        print(f"📊 Data Files:")
        print(f"   Stock CSV files: {len(csv_files)}")
        print(f"   Database files: {len(db_files)}")
        
        if csv_files:
            print("\n   Available stocks:")
            for csv_file in sorted(csv_files)[:10]:  # Show first 10
                name = csv_file.stem
                size_kb = csv_file.stat().st_size / 1024
                print(f"     • {name} ({size_kb:.1f} KB)")
            if len(csv_files) > 10:
                print(f"     ... and {len(csv_files) - 10} more")
    else:
        print("📊 No data directory found")
    
    # Check reports directory
    report_dir = Path("report")
    if report_dir.exists():
        reports = list(report_dir.glob("*"))
        print(f"\n📄 Generated Reports: {len(reports)}")
        
        if reports:
            # Group by type
            html_reports = [r for r in reports if r.suffix == '.html']
            txt_reports = [r for r in reports if r.suffix == '.txt']
            csv_reports = [r for r in reports if r.suffix == '.csv']
            
            print(f"   HTML reports: {len(html_reports)}")
            print(f"   Text reports: {len(txt_reports)}")
            print(f"   CSV summaries: {len(csv_reports)}")
            
            # Show latest reports
            if reports:
                print("\n   Latest reports:")
                latest_reports = sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
                for report in latest_reports:
                    mtime = datetime.fromtimestamp(report.stat().st_mtime)
                    size_kb = report.stat().st_size / 1024
                    print(f"     • {report.name} ({size_kb:.1f} KB) - {mtime.strftime('%Y-%m-%d %H:%M')}")
    else:
        print("\n📄 No reports directory found")
    
    # Check system files
    print(f"\n🔧 System Components:")
    components = [
        ("main.py", "Main application entry point"),
        ("config.py", "Configuration management"),
        ("simple_report_generator.py", "Enhanced report generator"),
        ("create_sample_data.py", "Sample data generator"),
        ("stock_data_crawler.py", "Data crawler"),
        ("quantitative_analysis.py", "Quantitative analysis"),
        ("news_sentiment.py", "News sentiment analysis"),
        ("model_processing.py", "AI model processing"),
        ("run_enhanced_reports.py", "Enhanced reporting runner"),
    ]
    
    for filename, description in components:
        if Path(filename).exists():
            size_kb = Path(filename).stat().st_size / 1024
            print(f"   ✅ {filename} ({size_kb:.1f} KB) - {description}")
        else:
            print(f"   ❌ {filename} - {description}")
    
    print(f"\n🚀 Quick Start Commands:")
    print(f"   Generate reports: python run_enhanced_reports.py")
    print(f"   Create sample data: python create_sample_data.py")
    print(f"   Run main application: python main.py")
    
    print(f"\n📖 Documentation:")
    docs = ["README.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "LICENSE"]
    for doc in docs:
        if Path(doc).exists():
            print(f"   📄 {doc}")
    
    print("\n" + "=" * 60)
    print("System overview complete!")

if __name__ == "__main__":
    show_system_overview()
