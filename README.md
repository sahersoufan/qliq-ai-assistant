# QLIQ AI Assistant

QLIQ AI Assistant is an intelligent assistant that provides personalized product and gig recommendations, answers questions, and helps users navigate the QLIQ platform. It leverages advanced AI technologies including retrieval-augmented generation (RAG), embedding-based recommendations, and query classification to deliver a seamless user experience.

## 🌟 Features

- **Intelligent Question Answering**: Ask questions about products, gigs, or platform information and get accurate, context-aware responses
- **Personalized Recommendations**: Receive tailored product and gig recommendations based on your profile and interests
- **Interactive Onboarding**: Chat with the AI assistant to get started with the platform
- **Bias Detection**: Ethical AI implementation that detects and warns about potential biases in recommendations
- **System Metrics**: Monitor performance and usage statistics
- **Classifier Comparison**: Compare different query classification approaches

## 🏗️ Architecture

The project is organized into two main components:

### Backend (Python/FastAPI)

- **API Layer** (`interface/api/`): RESTful endpoints for interacting with the assistant
- **Domain Layer** (`domain/`): Core business logic and services
  - Query processing and classification
  - Recommendation algorithms
  - Bias detection
- **Infrastructure Layer** (`infrastructure/`): Technical implementations
  - Vector databases (ChromaDB)
  - LLM integration (AWS Bedrock)
  - Machine learning models
- **Application Layer** (`app/`): Application setup and configuration

### Frontend (React/Vite)

- **Pages**: React components for different features
- **API Services**: JavaScript functions for communicating with the backend
- **Styling**: CSS for the user interface

### Data Flow

1. User submits a query through the frontend
2. Backend classifies the query (FAQ, Product, Gig, or General)
3. Relevant information is retrieved from vector databases
4. LLM generates a response using the retrieved context
5. Response is returned to the user

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **AWS Account** with access to Bedrock
- **Git** for cloning the repository

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd qliq-ai-assistant
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Using venv
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=your_aws_region
   BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
   
   # Optional: Uncomment to override defaults
   #EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   #CHROMA_DB_DIR=./data/chroma
   ```

5. **Run the backend**:
   ```bash
   python -m app.main
   ```
   The backend API will be available at http://localhost:8000

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   The frontend will be available at http://localhost:5173

## 📊 Data

The application uses several JSON files in the `data/` directory:

- `products.json`: Product catalog
- `gigs.json`: Available gigs
- `users.json`: User profiles
- `platform_docs.json`: Platform documentation
- `user_guides.json`: User guides

These files are loaded into vector databases at application startup.

## 🔍 API Documentation

When the backend is running, API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Postman Collection**: A Postman collection is available in the `docs` folder for testing the API endpoints
- **Demo Video**: A demonstration video is available in the `docs` folder called `demo.mkv`

## 🧪 Testing

Run the test suite with:
```bash
pytest
```

## 🏗️ Building for Production

### Backend

For production deployment, consider using Gunicorn or Uvicorn with a process manager:
```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend

Build the frontend for production:
```bash
cd frontend
npm run build
```
This creates a `dist` directory with optimized assets that can be served by any static file server.

## 🔧 Configuration

### Backend Configuration

The backend can be configured through environment variables in the `.env` file:

- **AWS_ACCESS_KEY_ID**: AWS access key for Bedrock
- **AWS_SECRET_ACCESS_KEY**: AWS secret key for Bedrock
- **AWS_REGION**: AWS region for Bedrock
- **BEDROCK_MODEL_ID**: Bedrock model ID to use
- **EMBEDDING_MODEL**: Model for generating embeddings (default: all-MiniLM-L6-v2)
- **CHROMA_DB_DIR**: Directory for ChromaDB files (default: ./data/chroma)

### Frontend Configuration

The frontend is configured to proxy API requests to the backend server running on http://localhost:8000. This is configured in the `vite.config.js` file.

To change the backend URL, update the `target` property in the proxy configuration.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

[Specify your license here]

## 📞 Support

For support, please [provide contact information or support channels].