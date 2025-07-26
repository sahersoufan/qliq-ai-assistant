import { useState, useEffect } from 'react';
import { getMetrics } from '../services/api';

function Metrics() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshInterval, setRefreshInterval] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(false);

  const fetchMetrics = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await getMetrics();
      setMetrics(response);
    } catch (err) {
      console.error('Error fetching metrics:', err);
      setError('Failed to fetch metrics. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchMetrics();
  }, []);

  // Set up auto-refresh
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(fetchMetrics, 10000); // Refresh every 10 seconds
      setRefreshInterval(interval);
    } else if (refreshInterval) {
      clearInterval(refreshInterval);
      setRefreshInterval(null);
    }
    
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, [autoRefresh]);

  const toggleAutoRefresh = () => {
    setAutoRefresh(!autoRefresh);
  };

  const renderMetricValue = (value) => {
    if (typeof value === 'object' && value !== null) {
      return (
        <ul>
          {Object.entries(value).map(([key, val]) => (
            <li key={key}>
              <strong>{key}:</strong> {renderMetricValue(val)}
            </li>
          ))}
        </ul>
      );
    }
    
    return String(value);
  };

  return (
    <div className="container">
      <h2>System Metrics</h2>
      <p>View performance metrics and system statistics</p>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <button onClick={fetchMetrics} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh Metrics'}
        </button>
        
        <div>
          <label>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={toggleAutoRefresh}
            />
            Auto-refresh (10s)
          </label>
        </div>
      </div>
      
      {error && <div className="error">{error}</div>}
      
      {loading && <div>Loading metrics...</div>}
      
      {metrics && !loading && (
        <div className="card">
          <h3>Current Metrics</h3>
          
          <div style={{ textAlign: 'left' }}>
            {Object.entries(metrics).map(([category, categoryMetrics]) => (
              <div key={category} style={{ marginBottom: '2rem' }}>
                <h4>{category}</h4>
                <ul>
                  {Object.entries(categoryMetrics).map(([key, value]) => (
                    <li key={key}>
                      <strong>{key}:</strong> {renderMetricValue(value)}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Metrics;