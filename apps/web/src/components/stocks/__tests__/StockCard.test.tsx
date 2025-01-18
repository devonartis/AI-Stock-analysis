import { render, screen } from '@/test/test-utils';
import { StockCard } from '../StockCard';

describe('StockCard', () => {
  const renderStockCard = (props = {}) => {
    const defaultProps = {
      symbol: 'AAPL',
      price: 150.50,
      change: 2.50,
      changePercent: 1.67,
      ...props
    };
    return render(<StockCard {...defaultProps} />);
  };

  it('displays stock symbol and price', () => {
    renderStockCard();
    expect(screen.getByText('AAPL')).toBeInTheDocument();
    expect(screen.getByText('$150.50')).toBeInTheDocument();
  });

  it('displays positive changes in green', () => {
    renderStockCard();
    const changeContainer = screen.getByText('+2.50').parentElement;
    expect(changeContainer).toHaveClass('text-green-600');
  });

  it('displays negative changes in red', () => {
    renderStockCard({ change: -2.50, changePercent: -1.67 });
    const changeContainer = screen.getByText('-2.50').parentElement;
    expect(changeContainer).toHaveClass('text-red-600');
  });
});
