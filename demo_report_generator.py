import pandas as pd
import os
import datetime
import logging
import sqlite3
import numpy as np
from quantitative_analysis import StockAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('report_demo.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_stock_data():
    """Get stock data with technical indicators"""
    analyzer = StockAnalyzer()
    
    # Get all stocks from database
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT stock_code, stock_name FROM stock_info")
    stocks = cursor.fetchall()
    conn.close()
    
    all_data = []
    
    for stock_code, stock_name in stocks:
        try:
            # Analyze stock and get technical indicators
            df = analyzer.analyze_stock(stock_code)
            if df is not None and len(df) > 0:
                # Get latest data
                latest = df.iloc[-1]
                
                stock_info = {
                    '代码': stock_code,
                    '公司名称': stock_name,
                    '最新价': latest.get('收盘', 0),
                    '涨跌幅': latest.get('涨跌幅', 0),
                    '换手率': latest.get('换手率', 0),
                    '成交额': latest.get('成交额', 0),
                    '成交量': latest.get('成交量', 0),
                    'MA_5': latest.get('MA_5', 0),
                    'MA_10': latest.get('MA_10', 0),
                    'MA_20': latest.get('MA_20', 0),
                    'MA_60': latest.get('MA_60', 0),
                    'RSI_6': latest.get('RSI_6', 50),
                    'RSI_12': latest.get('RSI_12', 50),
                    'RSI_24': latest.get('RSI_24', 50),
                    'MACD': latest.get('MACD', 0),
                    'MACD_signal': latest.get('MACD_signal', 0),
                    'MACD_hist': latest.get('MACD_hist', 0),
                    'KDJ_K': latest.get('STOCH_K', 50),
                    'KDJ_D': latest.get('STOCH_D', 50),
                    'KDJ_J': latest.get('STOCH_K', 50) * 3 - latest.get('STOCH_D', 50) * 2,
                    'BB_upper': latest.get('BB_upper', 0),
                    'BB_middle': latest.get('BB_middle', 0),
                    'BB_lower': latest.get('BB_lower', 0),
                    'BB_width': ((latest.get('BB_upper', 0) - latest.get('BB_lower', 0)) / latest.get('BB_middle', 1)) * 100 if latest.get('BB_middle', 0) > 0 else 0,
                    'ATR': latest.get('ATR', 0),
                    'ADX': latest.get('ADX', 0),
                    'VOLATILITY': latest.get('VOLATILITY', 0)
                }
                
                # Generate mock AI analysis based on technical indicators
                stock_info.update(generate_mock_analysis(stock_info))
                
                all_data.append(stock_info)
                logger.info(f"Processed {stock_name}({stock_code})")
                
        except Exception as e:
            logger.error(f"Error processing {stock_name}({stock_code}): {e}")
    
    return all_data

def generate_mock_analysis(stock_info):
    """Generate mock AI analysis based on technical indicators"""
    
    # Calculate basic score based on technical indicators
    score = 50  # Base score
    
    # RSI analysis
    rsi_12 = stock_info.get('RSI_12', 50)
    if 30 <= rsi_12 <= 70:
        score += 10
    elif rsi_12 < 30:
        score += 15  # Oversold, potential buy
    elif rsi_12 > 70:
        score -= 5   # Overbought
    
    # MACD analysis
    macd = stock_info.get('MACD', 0)
    macd_signal = stock_info.get('MACD_signal', 0)
    if macd > macd_signal:
        score += 8
    else:
        score -= 3
    
    # Moving average analysis
    price = stock_info.get('最新价', 0)
    ma_20 = stock_info.get('MA_20', 0)
    if price > ma_20:
        score += 5
    else:
        score -= 3
    
    # Volume analysis
    turnover = stock_info.get('换手率', 0)
    if 2 <= turnover <= 8:
        score += 5
    
    # Volatility analysis
    volatility = stock_info.get('VOLATILITY', 0)
    if volatility < 30:
        score += 3
    elif volatility > 50:
        score -= 5
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    # Generate recommendation based on score
    if score >= 80:
        recommendation = "强烈推荐"
        risk_level = "低风险"
    elif score >= 70:
        recommendation = "推荐"
        risk_level = "中低风险"
    elif score >= 60:
        recommendation = "观察"
        risk_level = "中等风险"
    elif score >= 50:
        recommendation = "谨慎"
        risk_level = "中高风险"
    else:
        recommendation = "不推荐"
        risk_level = "高风险"
    
    # Generate detailed analysis
    analysis_text = f"""
技术分析显示，该股票当前RSI为{rsi_12:.2f}，{'处于超买区间' if rsi_12 > 70 else '处于超卖区间' if rsi_12 < 30 else '处于合理区间'}。
MACD指标显示{'多头趋势' if macd > macd_signal else '空头趋势'}，建议{'持续关注' if macd > macd_signal else '谨慎操作'}。
股价{'高于' if price > ma_20 else '低于'}20日均线，显示{'上升趋势' if price > ma_20 else '下降趋势'}。
换手率为{turnover:.2f}%，{'活跃度适中' if 2 <= turnover <= 8 else '活跃度较高' if turnover > 8 else '活跃度较低'}。
"""
    
    fundamental_analysis = f"""
基于技术指标分析，该股票的综合评分为{score}分。
从波动率{volatility:.2f}%来看，该股票属于{risk_level}类别。
建议投资者根据个人风险承受能力进行决策。
"""
    
    trade_advice = f"""
基于当前技术指标，建议{recommendation}。
如果选择投资，建议分批建仓，控制好仓位。
止损位可设置在{price * 0.9:.2f}元附近。
目标价位在{price * 1.1:.2f}元-{price * 1.2:.2f}元区间。
"""
    
    risk_warning = f"""
投资有风险，入市需谨慎。
该股票当前风险等级为{risk_level}。
建议密切关注市场变化和公司基本面情况。
请根据自身投资目标和风险承受能力做出决策。
"""
    
    return {
        '评分': score,
        '建议': recommendation,
        '分析': analysis_text.strip(),
        'fundamental_analysis': fundamental_analysis.strip(),
        'trade_advice': trade_advice.strip(),
        'risk_warning': risk_warning.strip()
    }

def generate_enhanced_report(stock_data):
    """Generate comprehensive HTML and text reports"""
    
    # Sort by score
    sorted_data = sorted(stock_data, key=lambda x: x['评分'], reverse=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate text report
    text_report = generate_text_report(sorted_data, timestamp)
    
    # Generate HTML report
    html_report = generate_html_report(sorted_data, timestamp)
    
    # Generate CSV summary
    csv_report = generate_csv_summary(sorted_data)
    
    # Save reports
    os.makedirs('report', exist_ok=True)
    
    timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save text report
    text_path = f'report/stock_analysis_{timestamp_file}.txt'
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text_report)
    
    # Save HTML report
    html_path = f'report/stock_analysis_{timestamp_file}.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    # Save CSV summary
    csv_path = f'report/stock_summary_{timestamp_file}.csv'
    csv_report.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    return text_path, html_path, csv_path

def generate_text_report(sorted_data, timestamp):
    """Generate detailed text report"""
    
    report = f"""
╔══════════════════════════════════════════════════════════════════════════════
║                    智能股票分析报告 - {timestamp}
╚══════════════════════════════════════════════════════════════════════════════

📊 分析概要
────────────────────────────────────────────────────────────────────────────────
本次分析共涵盖 {len(sorted_data)} 只股票
最高评分: {sorted_data[0]['评分'] if sorted_data else 0} 分
平均评分: {sum(s['评分'] for s in sorted_data) / len(sorted_data):.1f} 分
推荐股票: {len([s for s in sorted_data if s['评分'] >= 70])} 只

"""
    
    for i, stock in enumerate(sorted_data, 1):
        report += f"""
╔══════════════════════════════════════════════════════════════════════════════
║ 【{i}】{stock['公司名称']} ({stock['代码']}) - 评分: {stock['评分']}/100
╚══════════════════════════════════════════════════════════════════════════════

🎯 投资建议: {stock['建议']}

📈 基础行情数据
────────────────────────────────────────────────────────────────────────────────
最新价格: {stock['最新价']:.2f} 元
涨跌幅度: {stock['涨跌幅']:.2f}%
换手率:   {stock['换手率']:.2f}%
成交额:   {stock['成交额']/10000:.2f} 万元
成交量:   {stock['成交量']/10000:.2f} 万股

📊 技术指标分析
────────────────────────────────────────────────────────────────────────────────
移动平均线:
  MA5:  {stock['MA_5']:.2f}    MA10: {stock['MA_10']:.2f}
  MA20: {stock['MA_20']:.2f}   MA60: {stock['MA_60']:.2f}

相对强弱指数 (RSI):
  RSI6:  {stock['RSI_6']:.2f}   RSI12: {stock['RSI_12']:.2f}   RSI24: {stock['RSI_24']:.2f}

MACD 指标:
  MACD:     {stock['MACD']:.4f}
  信号线:   {stock['MACD_signal']:.4f}
  柱状图:   {stock['MACD_hist']:.4f}

KDJ 指标:
  K值: {stock['KDJ_K']:.2f}    D值: {stock['KDJ_D']:.2f}    J值: {stock['KDJ_J']:.2f}

布林带指标:
  上轨: {stock['BB_upper']:.2f}   中轨: {stock['BB_middle']:.2f}   下轨: {stock['BB_lower']:.2f}
  带宽: {stock['BB_width']:.2f}%

其他技术指标:
  ATR (平均真实波幅): {stock['ATR']:.3f}
  ADX (趋势强度):     {stock['ADX']:.2f}
  波动率:            {stock['VOLATILITY']:.2f}%

🔍 技术面分析
────────────────────────────────────────────────────────────────────────────────
{stock['分析']}

📋 基本面分析
────────────────────────────────────────────────────────────────────────────────
{stock['fundamental_analysis']}

💡 交易建议
────────────────────────────────────────────────────────────────────────────────
{stock['trade_advice']}

⚠️  风险提示
────────────────────────────────────────────────────────────────────────────────
{stock['risk_warning']}

"""
    
    report += f"""

╔══════════════════════════════════════════════════════════════════════════════
║                              报告总结
╚══════════════════════════════════════════════════════════════════════════════

📊 投资建议分布:
────────────────────────────────────────────────────────────────────────────────
"""
    
    recommendations = {}
    for stock in sorted_data:
        rec = stock['建议']
        recommendations[rec] = recommendations.get(rec, 0) + 1
    
    for rec, count in recommendations.items():
        report += f"{rec}: {count} 只股票\n"
    
    report += f"""
📈 评分区间分布:
────────────────────────────────────────────────────────────────────────────────
90-100分: {len([s for s in sorted_data if s['评分'] >= 90])} 只
80-89分:  {len([s for s in sorted_data if 80 <= s['评分'] < 90])} 只
70-79分:  {len([s for s in sorted_data if 70 <= s['评分'] < 80])} 只
60-69分:  {len([s for s in sorted_data if 60 <= s['评分'] < 70])} 只
50-59分:  {len([s for s in sorted_data if 50 <= s['评分'] < 60])} 只
50分以下: {len([s for s in sorted_data if s['评分'] < 50])} 只

⚠️  免责声明
────────────────────────────────────────────────────────────────────────────────
本报告仅供参考，不构成投资建议。投资者应根据自身情况做出独立判断。
投资有风险，入市需谨慎。过往业绩不代表未来表现。

报告生成时间: {timestamp}
分析方法: 技术指标量化分析 + AI智能评分
数据来源: A股市场公开数据

╚══════════════════════════════════════════════════════════════════════════════
"""
    
    return report

def generate_html_report(sorted_data, timestamp):
    """Generate HTML report"""
    
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能股票分析报告 - {timestamp}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .stock-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
            padding: 20px;
            background: #fafafa;
        }}
        .stock-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        .metric-box {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }}
        .score {{
            font-size: 2em;
            font-weight: bold;
            color: #4CAF50;
        }}
        .recommendation {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
        }}
        .recommend {{ background-color: #4CAF50; }}
        .observe {{ background-color: #FF9800; }}
        .caution {{ background-color: #f44336; }}
        .strong-recommend {{ background-color: #2196F3; }}
        .not-recommend {{ background-color: #9E9E9E; }}
        .technical-indicators {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }}
        .indicator {{
            background: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            border: 1px solid #eee;
        }}
        .summary {{
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .chart-container {{
            margin: 20px 0;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 智能股票分析报告</h1>
            <p>生成时间: {timestamp}</p>
            <div style="margin-top: 15px;">
                <span style="background: #4CAF50; color: white; padding: 8px 16px; border-radius: 20px; margin: 0 10px;">
                    📊 共分析 {len(sorted_data)} 只股票
                </span>
                <span style="background: #2196F3; color: white; padding: 8px 16px; border-radius: 20px; margin: 0 10px;">
                    🏆 推荐 {len([s for s in sorted_data if s['评分'] >= 70])} 只
                </span>
            </div>
        </div>
        
        <div class="summary">
            <h2>📈 分析概要</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div>
                    <h3>最高评分</h3>
                    <div style="font-size: 2em; font-weight: bold;">{sorted_data[0]['评分'] if sorted_data else 0} 分</div>
                </div>
                <div>
                    <h3>平均评分</h3>
                    <div style="font-size: 2em; font-weight: bold;">{sum(s['评分'] for s in sorted_data) / len(sorted_data):.1f} 分</div>
                </div>
                <div>
                    <h3>推荐股票</h3>
                    <div style="font-size: 2em; font-weight: bold;">{len([s for s in sorted_data if s['评分'] >= 70])} 只</div>
                </div>
            </div>
        </div>

        <h2>📋 股票排行榜</h2>
        <table>
            <thead>
                <tr>
                    <th>排名</th>
                    <th>股票代码</th>
                    <th>公司名称</th>
                    <th>评分</th>
                    <th>建议</th>
                    <th>最新价</th>
                    <th>涨跌幅</th>
                    <th>换手率</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for i, stock in enumerate(sorted_data, 1):
        rec_class = {
            '强烈推荐': 'strong-recommend',
            '推荐': 'recommend', 
            '观察': 'observe',
            '谨慎': 'caution',
            '不推荐': 'not-recommend'
        }.get(stock['建议'], 'observe')
        
        html += f"""
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>{stock['代码']}</td>
                    <td>{stock['公司名称']}</td>
                    <td><span class="score">{stock['评分']}</span></td>
                    <td><span class="recommendation {rec_class}">{stock['建议']}</span></td>
                    <td>{stock['最新价']:.2f}</td>
                    <td style="color: {'green' if stock['涨跌幅'] >= 0 else 'red'};">{stock['涨跌幅']:.2f}%</td>
                    <td>{stock['换手率']:.2f}%</td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
        
        <h2>📊 详细分析报告</h2>
"""
    
    for i, stock in enumerate(sorted_data, 1):
        rec_class = {
            '强烈推荐': 'strong-recommend',
            '推荐': 'recommend', 
            '观察': 'observe',
            '谨慎': 'caution',
            '不推荐': 'not-recommend'
        }.get(stock['建议'], 'observe')
        
        html += f"""
        <div class="stock-card">
            <div class="stock-header">
                <h3>【{i}】{stock['公司名称']} ({stock['代码']})</h3>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="score">{stock['评分']} 分</span>
                    <span class="recommendation {rec_class}">{stock['建议']}</span>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-box">
                    <h4>💰 基础行情</h4>
                    <p><strong>最新价:</strong> {stock['最新价']:.2f} 元</p>
                    <p><strong>涨跌幅:</strong> <span style="color: {'green' if stock['涨跌幅'] >= 0 else 'red'};">{stock['涨跌幅']:.2f}%</span></p>
                    <p><strong>成交额:</strong> {stock['成交额']/10000:.2f} 万元</p>
                    <p><strong>换手率:</strong> {stock['换手率']:.2f}%</p>
                </div>
                
                <div class="metric-box">
                    <h4>📈 移动平均线</h4>
                    <div class="technical-indicators">
                        <div class="indicator">MA5<br><strong>{stock['MA_5']:.2f}</strong></div>
                        <div class="indicator">MA10<br><strong>{stock['MA_10']:.2f}</strong></div>
                        <div class="indicator">MA20<br><strong>{stock['MA_20']:.2f}</strong></div>
                        <div class="indicator">MA60<br><strong>{stock['MA_60']:.2f}</strong></div>
                    </div>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-box">
                    <h4>📊 RSI 指标</h4>
                    <div class="technical-indicators">
                        <div class="indicator">RSI6<br><strong>{stock['RSI_6']:.1f}</strong></div>
                        <div class="indicator">RSI12<br><strong>{stock['RSI_12']:.1f}</strong></div>
                        <div class="indicator">RSI24<br><strong>{stock['RSI_24']:.1f}</strong></div>
                    </div>
                </div>
                
                <div class="metric-box">
                    <h4>🎯 MACD 指标</h4>
                    <p><strong>MACD:</strong> {stock['MACD']:.4f}</p>
                    <p><strong>信号线:</strong> {stock['MACD_signal']:.4f}</p>
                    <p><strong>柱状图:</strong> {stock['MACD_hist']:.4f}</p>
                </div>
            </div>
            
            <div class="metric-box">
                <h4>🔍 技术面分析</h4>
                <p>{stock['分析']}</p>
            </div>
            
            <div class="metric-box">
                <h4>💡 交易建议</h4>
                <p>{stock['trade_advice']}</p>
            </div>
            
            <div class="metric-box">
                <h4>⚠️ 风险提示</h4>
                <p>{stock['risk_warning']}</p>
            </div>
        </div>
"""
    
    # Add summary statistics
    recommendations = {}
    for stock in sorted_data:
        rec = stock['建议']
        recommendations[rec] = recommendations.get(rec, 0) + 1
    
    html += f"""
        <div class="summary">
            <h2>📊 统计总结</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div>
                    <h3>投资建议分布</h3>
"""
    
    for rec, count in recommendations.items():
        html += f"<p>{rec}: {count} 只</p>"
    
    html += f"""
                </div>
                <div>
                    <h3>评分区间分布</h3>
                    <p>90-100分: {len([s for s in sorted_data if s['评分'] >= 90])} 只</p>
                    <p>80-89分: {len([s for s in sorted_data if 80 <= s['评分'] < 90])} 只</p>
                    <p>70-79分: {len([s for s in sorted_data if 70 <= s['评分'] < 80])} 只</p>
                    <p>60-69分: {len([s for s in sorted_data if 60 <= s['评分'] < 70])} 只</p>
                    <p>50分以下: {len([s for s in sorted_data if s['评分'] < 50])} 只</p>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #f9f9f9; border-radius: 10px; text-align: center;">
            <h3>⚠️ 免责声明</h3>
            <p>本报告仅供参考，不构成投资建议。投资者应根据自身情况做出独立判断。</p>
            <p>投资有风险，入市需谨慎。过往业绩不代表未来表现。</p>
            <p><small>报告生成时间: {timestamp} | 数据来源: A股市场公开数据</small></p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def generate_csv_summary(sorted_data):
    """Generate CSV summary"""
    
    summary_data = []
    for i, stock in enumerate(sorted_data, 1):
        summary_data.append({
            '排名': i,
            '股票代码': stock['代码'],
            '公司名称': stock['公司名称'],
            '评分': stock['评分'],
            '投资建议': stock['建议'],
            '最新价': stock['最新价'],
            '涨跌幅(%)': stock['涨跌幅'],
            '换手率(%)': stock['换手率'],
            '成交额(万元)': stock['成交额'] / 10000,
            'RSI12': stock['RSI_12'],
            'MACD': stock['MACD'],
            'MA20': stock['MA_20'],
            '波动率(%)': stock['VOLATILITY']
        })
    
    return pd.DataFrame(summary_data)

def main():
    """Main function to generate comprehensive reports"""
    
    logger.info("开始生成股票分析报告...")
    
    try:
        # Get stock data with analysis
        logger.info("获取股票数据并进行技术分析...")
        stock_data = get_stock_data()
        
        if not stock_data:
            logger.error("未找到任何股票数据")
            return
        
        logger.info(f"成功分析 {len(stock_data)} 只股票")
        
        # Generate reports
        logger.info("生成分析报告...")
        text_path, html_path, csv_path = generate_enhanced_report(stock_data)
        
        # Display results
        print("\n" + "="*80)
        print("🎉 股票分析报告生成完成!")
        print("="*80)
        print(f"📄 详细文本报告: {text_path}")
        print(f"🌐 HTML可视化报告: {html_path}")
        print(f"📊 CSV数据摘要: {csv_path}")
        print("="*80)
        
        # Show top recommendations
        top_5 = sorted(stock_data, key=lambda x: x['评分'], reverse=True)[:5]
        print("\n🏆 评分最高的5只股票:")
        print("-" * 60)
        for i, stock in enumerate(top_5, 1):
            print(f"{i}. {stock['公司名称']}({stock['代码']}) - 评分: {stock['评分']} - {stock['建议']}")
        
        print(f"\n💡 推荐查看HTML报告获得最佳阅读体验: {html_path}")
        logger.info("报告生成完成")
        
    except Exception as e:
        logger.error(f"生成报告时出错: {e}")
        raise

if __name__ == "__main__":
    main()
