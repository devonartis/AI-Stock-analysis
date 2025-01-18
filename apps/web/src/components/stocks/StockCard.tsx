import React from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { StockData } from '@/services/api';

type StockCardProps = StockData;

export function StockCard({ 
  symbol, 
  name,
  price, 
  change, 
  changePercent,
  sector,
  industry,
  marketCap,
  peRatio,
  dividendYield,
  fiftyTwoWeekHigh,
  fiftyTwoWeekLow,
  volume,
  avgVolume
}: StockCardProps) {
  const isPositive = change >= 0;
  const changeColor = isPositive ? 'text-green-600' : 'text-red-600';
  
  const formatNumber = (num: number | undefined, decimals = 2) => {
    if (num === undefined) return 'N/A';
    return num.toLocaleString(undefined, { 
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals 
    });
  };

  const formatLargeNumber = (num: number | undefined) => {
    if (num === undefined) return 'N/A';
    if (num >= 1e12) return `${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
    return formatNumber(num, 0);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex flex-col gap-1">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-2xl">{symbol}</span>
              {name && <span className="text-sm text-muted-foreground ml-2">{name}</span>}
            </div>
            <div className="text-2xl">${formatNumber(price)}</div>
          </div>
          {(change !== 0 || changePercent !== 0) && (
            <div className="flex justify-end">
              <div className={changeColor}>
                <span>{isPositive ? '+' : ''}{formatNumber(change)}</span>
                <span className="ml-2">({formatNumber(changePercent)}%)</span>
              </div>
            </div>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-2 gap-4 text-sm">
        {sector && (
          <div>
            <div className="text-muted-foreground">Sector</div>
            <div>{sector}</div>
          </div>
        )}
        {industry && (
          <div>
            <div className="text-muted-foreground">Industry</div>
            <div>{industry}</div>
          </div>
        )}
        {marketCap !== undefined && (
          <div>
            <div className="text-muted-foreground">Market Cap</div>
            <div>{formatLargeNumber(marketCap)}</div>
          </div>
        )}
        {peRatio !== undefined && (
          <div>
            <div className="text-muted-foreground">P/E Ratio</div>
            <div>{formatNumber(peRatio)}</div>
          </div>
        )}
        {dividendYield !== undefined && (
          <div>
            <div className="text-muted-foreground">Dividend Yield</div>
            <div>{formatNumber(dividendYield * 100)}%</div>
          </div>
        )}
        <div>
          <div className="text-muted-foreground">52 Week Range</div>
          <div>{formatNumber(fiftyTwoWeekLow)} - {formatNumber(fiftyTwoWeekHigh)}</div>
        </div>
        <div>
          <div className="text-muted-foreground">Volume</div>
          <div>{formatLargeNumber(volume)}</div>
        </div>
        <div>
          <div className="text-muted-foreground">Avg Volume</div>
          <div>{formatLargeNumber(avgVolume)}</div>
        </div>
      </CardContent>
    </Card>
  );
}
