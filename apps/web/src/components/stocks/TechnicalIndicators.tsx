import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface TechnicalIndicatorsProps {
  indicators: {
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
  className?: string;
}

function formatNumber(value: number): string {
  return value.toFixed(2);
}

function getIndicatorStatus(value: number, type: 'rsi' | 'macd'): 'neutral' | 'bullish' | 'bearish' {
  if (type === 'rsi') {
    if (value >= 70) return 'bearish';
    if (value <= 30) return 'bullish';
    return 'neutral';
  }
  
  // MACD interpretation
  return value > 0 ? 'bullish' : value < 0 ? 'bearish' : 'neutral';
}

export function TechnicalIndicators({ indicators, className }: TechnicalIndicatorsProps) {
  const { rsi, macd, sma_20, sma_50, sma_200, bollinger_bands } = indicators;
  const rsiStatus = getIndicatorStatus(rsi, 'rsi');
  const macdStatus = getIndicatorStatus(macd, 'macd');

  return (
    <Card className={cn("w-full", className)}>
      <CardHeader>
        <CardTitle>Technical Indicators</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4">
        {/* RSI and MACD Section */}
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <p className="text-sm font-medium">RSI</p>
            <p className={cn(
              "text-2xl font-bold",
              rsiStatus === 'bullish' && "text-green-500",
              rsiStatus === 'bearish' && "text-red-500"
            )}>
              {formatNumber(rsi)}
            </p>
            <p className="text-xs text-muted-foreground">
              {rsiStatus === 'bullish' ? 'Oversold' : rsiStatus === 'bearish' ? 'Overbought' : 'Neutral'}
            </p>
          </div>
          <div className="space-y-1">
            <p className="text-sm font-medium">MACD</p>
            <p className={cn(
              "text-2xl font-bold",
              macdStatus === 'bullish' && "text-green-500",
              macdStatus === 'bearish' && "text-red-500"
            )}>
              {formatNumber(macd)}
            </p>
            <p className="text-xs text-muted-foreground">
              {macdStatus === 'bullish' ? 'Bullish' : macdStatus === 'bearish' ? 'Bearish' : 'Neutral'}
            </p>
          </div>
        </div>

        {/* Moving Averages Section */}
        <div className="space-y-2">
          <p className="text-sm font-medium">Moving Averages</p>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">SMA 20</p>
              <p className="text-lg font-semibold">{formatNumber(sma_20)}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">SMA 50</p>
              <p className="text-lg font-semibold">{formatNumber(sma_50)}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">SMA 200</p>
              <p className="text-lg font-semibold">{formatNumber(sma_200)}</p>
            </div>
          </div>
        </div>

        {/* Bollinger Bands Section */}
        <div className="space-y-2">
          <p className="text-sm font-medium">Bollinger Bands</p>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div>
                <p className="text-sm text-muted-foreground">Upper Band</p>
                <p className="text-lg font-semibold">{formatNumber(bollinger_bands.upper)}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Middle Band</p>
                <p className="text-lg font-semibold">{formatNumber(bollinger_bands.middle)}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Lower Band</p>
                <p className="text-lg font-semibold">{formatNumber(bollinger_bands.lower)}</p>
              </div>
            </div>
            <div className="space-y-2">
              <div>
                <p className="text-sm text-muted-foreground">Bandwidth</p>
                <p className="text-lg font-semibold">{formatNumber(bollinger_bands.bandwidth)}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">%B</p>
                <p className="text-lg font-semibold">{formatNumber(bollinger_bands.percent_b)}</p>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
