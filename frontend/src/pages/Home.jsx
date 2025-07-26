import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { checkHealth } from '../services/api';

function Home() {
  const [status, setStatus] = useState('Loading...');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await checkHealth();
        setStatus(response.status);
      } catch (err) {
        console.error('Error checking health:', err);
        setError('Failed to connect to the server. Please try again later.');
      }
    };

    fetchStatus();
  }, []);

  return (
    <div className="container">
      <div className="card">
        <h2>Welcome to QLIQ AI Assistant</h2>
        <p>Your intelligent assistant for product and gig recommendations</p>
        
        <div style={{ margin: '2rem 0' }}>
          <h3>Server Status: {error ? 'Error' : status}</h3>
          {error && <p className="error">{error}</p>}
        </div>
        
        <p>Get started by exploring the following features:</p>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
          <Link to="/onboard" className="card">
            <h3>Onboarding</h3>
            <p>Get started with the AI assistant</p>
          </Link>
          
          <Link to="/ask" className="card">
            <h3>Ask Questions</h3>
            <p>Ask the AI assistant any question</p>
          </Link>
          
          <Link to="/recommendations" className="card">
            <h3>Recommendations</h3>
            <p>Get personalized product and gig recommendations</p>
          </Link>
          
          <Link to="/metrics" className="card">
            <h3>Metrics</h3>
            <p>View system metrics and performance</p>
          </Link>
          
          <Link to="/classifier-compare" className="card">
            <h3>Classifier Comparison</h3>
            <p>Compare different query classifiers</p>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;