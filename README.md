# Stock Analysis Application

A comprehensive stock analysis platform with a FastAPI backend and Next.js frontend.

## Project Structure

```
/stock_app/
├── backend/            # FastAPI backend
│   ├── app/           # Application code
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Core functionality
│   │   ├── schemas/   # Pydantic models
│   │   ├── services/  # Business logic
│   │   └── utils/     # Utilities
│   └── requirements.txt
├── apps/              # Frontend applications
│   └── web/          # Next.js web application
└── packages/         # Shared packages (future use)
```

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm 10+

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the development server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install root dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The web application will be available at `http://localhost:3000`

## Development

This project uses Turborepo for managing the monorepo structure:

- `npm run dev` - Start all applications in development mode
- `npm run build` - Build all applications
- `npm run lint` - Run linting for all applications
- `npm run format` - Format code using Prettier

## Features

### Backend
- Real-time stock data analysis
- Technical indicators calculation
- Historical data analysis
- Machine learning predictions
- News sentiment analysis

### Frontend
- Interactive stock charts
- Real-time price updates
- Technical analysis visualization
- Portfolio management
- News integration

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

[MIT License](LICENSE)
