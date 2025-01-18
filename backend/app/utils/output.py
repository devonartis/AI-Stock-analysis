import os
import json
from datetime import datetime
import mplfinance as mpf
import pandas as pd
from typing import Dict, Any

from ..models.stock import StockAnalysis

class OutputManager:
    def __init__(self, output_dir: str = 'output'):
        self.output_dir = output_dir
        self._ensure_output_dir()
        
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def _create_timestamp(self) -> str:
        """Create timestamp string for file names"""
        return datetime.now().strftime('%Y%m%d_%H%M%S')
            
    def save_analysis(self, analysis: StockAnalysis, technical_data: pd.DataFrame) -> Dict[str, str]:
        """
        Save analysis results to various file formats
        
        Returns:
            Dict mapping output type to file path
        """
        timestamp = self._create_timestamp()
        ticker = analysis.company_info.ticker
        output_files = {}
        
        # Save raw data to CSV
        csv_path = os.path.join(self.output_dir, f'{ticker}_analysis_{timestamp}.csv')
        technical_data.to_csv(csv_path)
        output_files['csv'] = csv_path
        
        # Save chart to PNG
        chart_path = os.path.join(self.output_dir, f'{ticker}_chart_{timestamp}.png')
        self._save_chart(technical_data, analysis.company_info.name, ticker, chart_path)
        output_files['chart'] = chart_path
        
        # Save summary to JSON
        json_path = os.path.join(self.output_dir, f'{ticker}_summary_{timestamp}.json')
        with open(json_path, 'w') as f:
            json.dump(analysis.model_dump(), f, indent=2, default=str)
        output_files['json'] = json_path
        
        # Save text summary
        txt_path = os.path.join(self.output_dir, f'{ticker}_summary_{timestamp}.txt')
        self._save_text_summary(analysis, txt_path)
        output_files['text'] = txt_path
        
        return output_files
        
    def _save_chart(self, data: pd.DataFrame, company_name: str, ticker: str, filepath: str):
        """Create and save technical analysis chart"""
        addplots = []
        
        # Only add indicators if they exist in the data
        if 'SMA_20' in data.columns and not data['SMA_20'].isna().all():
            addplots.append(mpf.make_addplot(data['SMA_20'], color='cyan', width=0.7))
        if 'SMA_50' in data.columns and not data['SMA_50'].isna().all():
            addplots.append(mpf.make_addplot(data['SMA_50'], color='magenta', width=0.7))
        if 'SMA_200' in data.columns and not data['SMA_200'].isna().all():
            addplots.append(mpf.make_addplot(data['SMA_200'], color='yellow', width=0.7))
        
        # Create figure with appropriate panel ratios
        has_volume = True
        has_rsi = 'RSI' in data.columns and not data['RSI'].isna().all()
        
        if has_rsi:
            addplots.append(mpf.make_addplot(data['RSI'], panel=2, color='white', ylabel='RSI'))
            panel_ratios = (6, 2, 2)  # Main chart, volume, RSI
        else:
            panel_ratios = (6, 2)  # Main chart and volume only
            
        kwargs = dict(
            type='candle',
            volume=has_volume,
            figsize=(15, 10),
            title=f'\n{company_name} ({ticker}) Stock Analysis',
            style='charles',
            addplot=addplots,
            volume_panel=1,
            panel_ratios=panel_ratios,
            main_panel=0,
            ylabel='Price (USD)'
        )
        
        mpf.plot(data, **kwargs, savefig=filepath)
        
    def _save_text_summary(self, analysis: StockAnalysis, filepath: str):
        """Save analysis summary in human-readable format"""
        with open(filepath, 'w') as f:
            f.write(f"{analysis.company_name} ({analysis.ticker}) Analysis\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Current Technical Indicators:\n")
            f.write(f"Current Price: ${analysis.current_price:.2f}\n")
            f.write(f"RSI: {analysis.technical_indicators.rsi:.2f}\n")
            f.write(f"SMA 20: ${analysis.technical_indicators.sma_20:.2f}\n")
            f.write(f"SMA 50: ${analysis.technical_indicators.sma_50:.2f}\n")
            f.write(f"SMA 200: ${analysis.technical_indicators.sma_200:.2f}\n\n")
            
            f.write("Price Statistics:\n")
            for stat, value in analysis.price_statistics.items():
                f.write(f"{stat.replace('_', ' ').title()}: {value:.2f}\n")
            
            f.write("\nCompany Information:\n")
            f.write(f"Sector: {analysis.company_info.sector or 'N/A'}\n")
            f.write(f"Industry: {analysis.company_info.industry or 'N/A'}\n")
            
            market_cap = analysis.company_info.market_cap
            market_cap_str = f"${market_cap:,.2f}" if market_cap else "N/A"
            f.write(f"Market Cap: {market_cap_str}\n")
            
            high = analysis.company_info.fifty_two_week_high
            high_str = f"${high:.2f}" if high else "N/A"
            f.write(f"52 Week High: {high_str}\n")
            
            low = analysis.company_info.fifty_two_week_low
            low_str = f"${low:.2f}" if low else "N/A"
            f.write(f"52 Week Low: {low_str}\n")
