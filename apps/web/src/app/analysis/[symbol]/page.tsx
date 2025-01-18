export default function StockAnalysisPage({
  params,
}: {
  params: { symbol: string };
}) {
  return (
    <div>
      <h1>Stock Analysis: {params.symbol}</h1>
    </div>
  );
}
