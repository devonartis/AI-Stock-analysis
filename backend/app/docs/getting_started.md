# Getting Started with Stock Analysis API

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stock-analysis-api
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

## Project Structure

The project follows a clear separation of concerns:

```
app/
├── api/          # API endpoints
├── core/         # Core configuration
├── models/       # Domain models
├── schemas/      # API schemas (DTOs)
├── services/     # Business logic
└── utils/        # Utilities
```

For a detailed explanation of the difference between models and schemas, see [Models vs Schemas](models_vs_schemas.md).

## Configuration

1. The application uses Pydantic settings for configuration. Default values are provided, but you can override them using environment variables.

2. Key configuration options:
```python
APP_NAME="Stock Analysis API"
API_V1_STR="/api/v1"
OUTPUT_DIR="output"
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. The API will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/api/v1/docs
- Alternative docs: http://localhost:8000/api/v1/redoc

## Quick Start Guide

### 1. Search for a Stock
```bash
curl "http://localhost:8000/api/v1/stocks/search/Apple"
```

### 2. Get Stock Information
```bash
curl "http://localhost:8000/api/v1/stocks/AAPL"
```

### 3. Analyze Stock
```bash
curl "http://localhost:8000/api/v1/stocks/AAPL/analysis?days=365"
```

## Development

### Code Organization

1. **API Endpoints** (`/api/v1/endpoints/`)
   - Define routes and handle HTTP requests
   - Use schemas for request/response validation
   - Inject services using FastAPI dependencies

2. **Domain Models** (`/models/`)
   - Implement business logic
   - Handle complex calculations
   - Manage internal state

3. **API Schemas** (`/schemas/`)
   - Define request/response structures
   - Validate API inputs
   - Generate API documentation

4. **Services** (`/services/`)
   - Implement business operations
   - Handle external integrations
   - Process data

### Adding New Features

1. Define schemas in `app/schemas/`
2. Implement business logic in `app/models/`
3. Create services in `app/services/`
4. Add endpoints in `app/api/v1/endpoints/`

### Testing

Run tests using pytest:
```bash
pytest
```

## Common Issues

1. **Import Errors**
   - Ensure you're in the virtual environment
   - Check if all dependencies are installed

2. **Configuration Issues**
   - Verify environment variables
   - Check permissions for output directory

3. **API Errors**
   - Check API documentation for correct endpoints
   - Verify input parameters
   - Ensure proper schema validation

## Next Steps

1. Explore the API documentation at `/api/v1/docs`
2. Review [Models vs Schemas](models_vs_schemas.md) guide
3. Check out the technical indicators and analysis results
4. Review the architecture documentation for deeper understanding

## Support

For issues and feature requests, please:
1. Check the documentation
2. Review troubleshooting guide
3. Submit an issue on GitHub
