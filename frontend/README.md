# QLIQ AI Assistant Frontend

This is the frontend for the QLIQ AI Assistant, a web application that provides AI-powered assistance for product and gig recommendations.

## Features

- **Home**: Welcome page with links to all features
- **Onboarding**: Chat with the AI assistant to get started
- **Ask**: Ask the AI assistant questions about products, gigs, or general information
- **Recommendations**: Get personalized product and gig recommendations
- **Metrics**: View system metrics and performance
- **Classifier Comparison**: Compare different query classifiers

## Technology Stack

- **React**: Frontend library for building user interfaces
- **React Router**: For navigation between pages
- **Axios**: For making API requests to the backend
- **Vite**: Build tool for faster development

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend server running on http://localhost:8000

### Installation

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn
   ```

3. Start the development server:
   ```
   npm run dev
   ```
   or
   ```
   yarn dev
   ```

4. Open your browser and navigate to http://localhost:5173

## API Integration

The frontend communicates with the backend API using the following endpoints:

- `GET /health`: Health check endpoint
- `POST /onboard`: Onboarding chat endpoint
- `POST /ask`: Question answering endpoint
- `GET /recommendations/{userId}`: Recommendations endpoint
- `GET /metrics`: System metrics endpoint
- `GET /classifier-compare`: Classifier comparison endpoint

## Configuration

The frontend is configured to proxy API requests to the backend server running on http://localhost:8000. This is configured in the `vite.config.js` file.

If you need to change the backend URL, update the `target` property in the proxy configuration in `vite.config.js`.

## Building for Production

To build the frontend for production:

```
npm run build
```
or
```
yarn build
```

This will create a `dist` directory with the compiled assets that can be served by any static file server.

## Project Structure

- `src/`: Source code directory
  - `main.jsx`: Entry point
  - `App.jsx`: Main component with routing
  - `index.css`: Global styles
  - `services/`: API service layer
    - `api.js`: API client and functions
  - `pages/`: Page components
    - `Home.jsx`: Home page
    - `Onboarding.jsx`: Onboarding page
    - `Ask.jsx`: Question answering page
    - `Recommendations.jsx`: Recommendations page
    - `Metrics.jsx`: Metrics page
    - `ClassifierComparison.jsx`: Classifier comparison page