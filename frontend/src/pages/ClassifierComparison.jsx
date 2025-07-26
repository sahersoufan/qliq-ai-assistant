import { useState, useEffect } from 'react';
import { compareClassifiers } from '../services/api';

function ClassifierComparison() {
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchComparison = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await compareClassifiers();
        setComparison(response);
      } catch (err) {
        console.error('Error comparing classifiers:', err);
        setError('Failed to compare classifiers. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchComparison();
  }, []);

  const getLabelColor = (label) => {
    switch (label) {
      case 'FAQ':
        return '#4caf50'; // Green
      case 'Product':
        return '#2196f3'; // Blue
      case 'Gig':
        return '#ff9800'; // Orange
      case 'General':
        return '#9e9e9e'; // Gray
      default:
        return '#000000'; // Black
    }
  };

  return (
    <div className="container">
      <h2>Classifier Comparison</h2>
      <p>Compare the performance of different query classifiers</p>
      
      {error && <div className="error">{error}</div>}
      
      {loading && <div>Loading comparison data...</div>}
      
      {comparison && !loading && (
        <div className="card">
          <h3>Classifier Comparison Results</h3>
          <p>Match Rate: <strong>{(comparison.match_rate * 100).toFixed(2)}%</strong></p>
          
          <div style={{ overflowX: 'auto', marginTop: '1rem' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ padding: '0.5rem', borderBottom: '1px solid #333', textAlign: 'left' }}>Query</th>
                  <th style={{ padding: '0.5rem', borderBottom: '1px solid #333', textAlign: 'center' }}>ML Classifier</th>
                  <th style={{ padding: '0.5rem', borderBottom: '1px solid #333', textAlign: 'center' }}>Rule-Based Classifier</th>
                  <th style={{ padding: '0.5rem', borderBottom: '1px solid #333', textAlign: 'center' }}>Match</th>
                </tr>
              </thead>
              <tbody>
                {comparison.results.map((result, index) => (
                  <tr key={index} style={{ backgroundColor: result.match ? 'rgba(76, 175, 80, 0.1)' : 'rgba(244, 67, 54, 0.1)' }}>
                    <td style={{ padding: '0.5rem', borderBottom: '1px solid #333' }}>{result.query}</td>
                    <td style={{ padding: '0.5rem', borderBottom: '1px solid #333', textAlign: 'center' }}>
                      <span style={{ 
                        backgroundColor: getLabelColor(result.ml_label),
                        color: 'white',
                        padding: '0.2rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.9rem'
                      }}>
                        {result.ml_label}
                      </span>
                    </td>
                    <td style={{ padding: '0.5rem', borderBottom: '1px solid #333', textAlign: 'center' }}>
                      <span style={{ 
                        backgroundColor: getLabelColor(result.rule_based_label),
                        color: 'white',
                        padding: '0.2rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.9rem'
                      }}>
                        {result.rule_based_label}
                      </span>
                    </td>
                    <td style={{ padding: '0.5rem', borderBottom: '1px solid #333', textAlign: 'center' }}>
                      {result.match ? '✅' : '❌'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div style={{ marginTop: '2rem' }}>
            <h4>Legend:</h4>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
              {['FAQ', 'Product', 'Gig', 'General'].map(label => (
                <div key={label} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ 
                    backgroundColor: getLabelColor(label),
                    width: '1rem',
                    height: '1rem',
                    display: 'inline-block',
                    borderRadius: '2px'
                  }}></span>
                  <span>{label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ClassifierComparison;