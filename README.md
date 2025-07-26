# QLIQ AI Assistant

QLIQ AI Assistant is an intelligent assistant that provides personalized product and gig recommendations, answers questions, and helps users navigate the QLIQ platform.

## Project Structure

The project is organized into two main components:

1. **Backend**: A FastAPI-based Python application that provides the AI functionality
2. **Frontend**: A React-based web application that provides a user interface for interacting with the AI assistant

### Backend Components

- **API Endpoints**: Defined in the `interface/api` directory
- **Domain Logic**: Business logic and services in the `domain` directory
- **Infrastructure**: Data storage, ML models, and utilities in the `infrastructure` directory
- **Application**: Main application setup in the `app` directory

### Frontend Components

- **Pages**: React components for different features
- **API Services**: JavaScript functions for communicating with the backend API
- **Styling**: CSS for the user interface

## Features

- **Health Check**: Verify the system is running properly
- **Onboarding**: Chat with the AI assistant to get started
- **Ask**: Ask the AI assistant questions about products, gigs, or general information
- **Recommendations**: Get personalized product and gig recommendations
- **Metrics**: View system metrics and performance
- **Classifier Comparison**: Compare different query classifiers

## Setup Instructions

### Backend Setup

1. Install Python 3.8 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables (copy `.env.example` to `.env` if available)
4. Run the application:
   ```
   python -m app.main
   ```
5. The backend API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Install Node.js dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm run dev
   ```
4. The frontend will be available at http://localhost:5173

## API Documentation

When the backend is running, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

For more detailed information about each component:

- See the backend code documentation in the respective module directories
- See the frontend README at `frontend/README.md`