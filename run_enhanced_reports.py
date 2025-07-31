#!/usr/bin/env python3
"""
AI Stock Selector - Enhanced Report Generator
智能股票筛选系统 - 增强报告生成器

This script generates comprehensive stock analysis reports including:
- Detailed text reports with technical analysis
- Interactive HTML reports with visualizations
- CSV summaries for data analysis

Usage:
    python run_enhanced_reports.py

Features:
- Technical indicator analysis (MA, RSI, MACD, KDJ, Bollinger Bands)
- AI-powered scoring and recommendations
- Multi-format output (TXT, HTML, CSV)
- Professional report formatting
"""

import os
import sys
import time
from pathlib import Path

def main():
    print("🎯 AI Stock Selector - Enhanced Report Generator")
    print("=" * 60)
    print("智能股票筛选系统 - 增强报告生成器")
    print("=" * 60)
    
    # Check if we have data
    data_dir = Path("data")
    if not data_dir.exists() or not any(data_dir.glob("*.csv")):
        print("⚠️  No stock data found. Setting up sample data...")
        print("正在设置示例数据...")
        
        try:
            import create_sample_data
            create_sample_data.create_sample_data()
            print("✅ Sample data created successfully!")
            print("示例数据创建成功！")
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            print("创建示例数据时出错")
            return
    
    print(f"\n📊 Found {len(list(data_dir.glob('*.csv')))} stock data files")
    print(f"发现 {len(list(data_dir.glob('*.csv')))} 个股票数据文件")
    
    # Generate reports
    print("\n🚀 Generating comprehensive reports...")
    print("正在生成综合分析报告...")
    
    start_time = time.time()
    
    try:
        import simple_report_generator
        simple_report_generator.main()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n⏱️  Report generation completed in {duration:.2f} seconds")
        print(f"报告生成完成，耗时 {duration:.2f} 秒")
        
        # List generated files
        report_dir = Path("report")
        latest_reports = sorted(report_dir.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True)[:3]
        
        print("\n📄 Generated Reports | 生成的报告:")
        print("-" * 40)
        for report in latest_reports:
            size_kb = report.stat().st_size / 1024
            print(f"  📁 {report.name} ({size_kb:.1f} KB)")
        
        # Find HTML report
        html_reports = list(report_dir.glob("*.html"))
        if html_reports:
            latest_html = max(html_reports, key=lambda x: x.stat().st_mtime)
            print(f"\n🌐 Best viewing experience: {latest_html}")
            print(f"最佳查看体验: {latest_html}")
            print("   Open this file in your web browser for interactive analysis")
            print("   在浏览器中打开此文件获得交互式分析体验")
        
        print("\n" + "=" * 60)
        print("✅ Report Generation Complete!")
        print("报告生成完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")
        print(f"生成报告时出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
