import { render, screen } from '@testing-library/react';

describe('Testing Setup', () => {
  it('can render a component and use jest-dom matchers', () => {
    render(<div data-testid="test-element">Test Setup Working</div>);
    
    const element = screen.getByTestId('test-element');
    expect(element).toBeInTheDocument();
    expect(element).toHaveTextContent('Test Setup Working');
  });
});
