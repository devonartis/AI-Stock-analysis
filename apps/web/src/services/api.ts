import { logger } from '@/utils/logger';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// This interface matches the actual response we get from the backend
interface BackendResponse {
  analysis: {
    company_info: {
      name: string;
      ticker: string;
      sector: string;
      industry: string;
      market_cap: number;
      fifty_two_week_high: number;
      fifty_two_week_low: number;
    };
    current_price: number;
    technical_indicators: {
      rsi: number;
      macd: number;
      sma_20: number;
      sma_50: number;
      sma_200: number;
      bollinger_bands: {
        upper: number;
        middle: number;
        lower: number;
        bandwidth: number;
        percent_b: number;
      };
    };
    price_statistics: {
      mean: number;
      std: number;
      min: number;
      max: number;
      median: number;
    };
    historical_prices: Array<{
      date: string;
      open: number;
      high: number;
      low: number;
      close: number;
      volume: number;
    }>;
    ticker: string;
    company_name: string;
    volume: number;
  };
  output_files: {
    csv: string;
    chart: string;
    json: string;
    text: string;
  };
  execution_time: number;
}

export interface StockData {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  name?: string;
  sector?: string;
  industry?: string;
  marketCap?: number;
  peRatio?: number;
  dividendYield?: number;
  fiftyTwoWeekHigh?: number;
  fiftyTwoWeekLow?: number;
  volume?: number;
  avgVolume?: number;
}

export async function getStockInfo(symbol: string): Promise<StockData> {
  logger.info(`Fetching stock data for symbol: ${symbol}`);
  
  try {
    const response = await fetch(`${API_BASE_URL}/stock/${symbol}/analysis`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      }
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        const error = `Stock symbol ${symbol} not found`;
        logger.warn(error);
        throw new Error(error);
      }
      const error = 'Failed to fetch stock data';
      logger.error(error, { status: response.status });
      throw new Error(error);
    }
    
    const data: BackendResponse = await response.json();
    logger.debug('Received stock data', { symbol, data });
    
    // Calculate daily change and percent from historical prices
    const prices = data.analysis.historical_prices;
    const lastPrice = prices[prices.length - 1].close;
    const prevPrice = prices[prices.length - 2].close;
    const change = lastPrice - prevPrice;
    const changePercent = (change / prevPrice) * 100;
    
    // Calculate average volume from historical prices
    const avgVolume = prices.reduce((sum, price) => sum + price.volume, 0) / prices.length;
    
    // Map the nested structure to our frontend model
    return {
      symbol: data.analysis.ticker,
      name: data.analysis.company_name,
      price: data.analysis.current_price,
      change: change,
      changePercent: changePercent,
      sector: data.analysis.company_info.sector,
      industry: data.analysis.company_info.industry,
      marketCap: data.analysis.company_info.market_cap,
      fiftyTwoWeekHigh: data.analysis.company_info.fifty_two_week_high,
      fiftyTwoWeekLow: data.analysis.company_info.fifty_two_week_low,
      volume: data.analysis.volume,
      avgVolume: avgVolume
    };
  } catch (error) {
    logger.error('Error in getStockInfo', { 
      symbol, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    });
    throw error;
  }
}
