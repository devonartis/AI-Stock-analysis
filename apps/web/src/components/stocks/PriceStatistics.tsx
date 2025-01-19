import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface PriceStatisticsProps {
  statistics: {
    mean: number;
    std: number;
    min: number;
    max: number;
    median: number;
  };
  className?: string;
}

function formatNumber(value: number): string {
  return value.toFixed(2);
}

export function PriceStatistics({ statistics, className }: PriceStatisticsProps) {
  const { mean, std, min, max, median } = statistics;

  return (
    <Card className={cn("w-full", className)}>
      <CardHeader>
        <CardTitle>Price Statistics</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Mean</p>
            <p className="text-lg font-semibold">${formatNumber(mean)}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Median</p>
            <p className="text-lg font-semibold">${formatNumber(median)}</p>
          </div>
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Min</p>
            <p className="text-lg font-semibold">${formatNumber(min)}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Max</p>
            <p className="text-lg font-semibold">${formatNumber(max)}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Std Dev</p>
            <p className="text-lg font-semibold">${formatNumber(std)}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
