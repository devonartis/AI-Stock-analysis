// frontend/src/utils/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function analyzeStock(ticker: string) {
  const response = await fetch(`${API_URL}/api/v1/stocks/analyze/${ticker}`);
  if (!response.ok) {
    throw new Error('Failed to analyze stock');
  }
  return response.json();
}