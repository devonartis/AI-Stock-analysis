# Stock Analysis Platform

An AI-driven stock analysis platform that democratizes trading decisions by combining technical analysis, machine learning, and natural language processing. The system provides explainable trading recommendations through a conversational interface, making complex market analysis accessible to traders of all experience levels.

## Features

### AI and ML Capabilities
- Explainable trading recommendations using LLMs
- ML-based stock movement predictions
- SHAP feature importance analysis
- Interactive Q&A about market conditions
- Natural language technical analysis
- Personalized risk assessment

### Technical Analysis
- Comprehensive technical indicators
- Pattern recognition
- Market trend analysis
- Trading signal generation
- Real-time data processing

### Data Integration
- Real-time market data
- News sentiment analysis
- Social media sentiment
- Historical price analysis
- Volume analysis

### User Experience
- Conversational interface
- Follow-up questions
- Educational content
- Strategy explanations
- Risk tolerance adaptation

## Quick Start

1. Clone the repository

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   NEWS_API_KEY=your_api_key
   OPENAI_API_KEY=your_openai_key  # For LLM features
   OUTPUT_DIR=path/to/output
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture

The backend is built with:
- FastAPI for high-performance API
- Pydantic AI for LLM integration
- ML pipeline for market analysis
- Redis for caching
- PostgreSQL for data persistence

## API Documentation

Once running, visit:
- OpenAPI docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Documentation
For detailed documentation, see [Project Documentation](docs/project_documentation.md)

## License
MIT License - See LICENSE file for details
