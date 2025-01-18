'use client'

import { useState } from 'react'
import { StockSearch } from "@/components/stocks/StockSearch"
import { StockCard } from "@/components/stocks/StockCard"
import { getStockInfo, type StockData } from "@/services/api"
import { logger } from '@/utils/logger'

export default function Home() {
  const [stockData, setStockData] = useState<StockData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (symbol: string) => {
    logger.info('User initiated stock search', { symbol });
    setLoading(true)
    setError(null)
    
    try {
      const data = await getStockInfo(symbol)
      logger.info('Successfully displayed stock data to user', { symbol });
      setStockData(data)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch stock data. Please try again.';
      logger.error('Error displaying stock data to user', { 
        symbol, 
        error: errorMessage 
      });
      setError(errorMessage)
      setStockData(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center p-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold">Stock Analysis</h1>
      </header>
      
      <main className="flex w-full max-w-4xl flex-col items-center gap-8">
        <section className="w-full">
          <StockSearch onSearch={handleSearch} />
        </section>
        
        <section className="w-full">
          {loading ? (
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            </div>
          ) : error ? (
            <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-600">
              {error}
            </div>
          ) : stockData ? (
            <StockCard {...stockData} />
          ) : (
            <div className="rounded-lg border p-4">
              <p className="text-muted-foreground">Enter a stock symbol above to see details</p>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}
