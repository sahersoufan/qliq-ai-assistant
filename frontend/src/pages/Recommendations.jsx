import { useState } from 'react';
import { getRecommendations } from '../services/api';

function Recommendations() {
  const [userId, setUserId] = useState('');
  const [topK, setTopK] = useState(5);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!userId.trim()) return;
    
    setLoading(true);
    setError(null);
    setRecommendations(null);
    
    try {
      // Get recommendations from the API
      const response = await getRecommendations(userId, topK);
      setRecommendations(response);
    } catch (err) {
      console.error('Error getting recommendations:', err);
      setError('Failed to get recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Recommendations</h2>
      <p>Get personalized product and gig recommendations</p>
      
      <form onSubmit={handleSubmit} className="form-group">
        <div className="form-group">
          <label htmlFor="userId">User ID:</label>
          <input
            id="userId"
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter user ID (e.g., user_002)"
            disabled={loading}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="topK">Number of recommendations:</label>
          <input
            id="topK"
            type="number"
            min="1"
            max="20"
            value={topK}
            onChange={(e) => setTopK(parseInt(e.target.value))}
            disabled={loading}
          />
        </div>
        
        <button type="submit" disabled={loading || !userId.trim()}>
          {loading ? 'Loading...' : 'Get Recommendations'}
        </button>
      </form>
      
      {error && <div className="error">{error}</div>}
      
      {recommendations && (
        <div className="card">
          <h3>Recommendations for User: {userId}</h3>
          
          {recommendations.bias_warnings && recommendations.bias_warnings.length > 0 && (
            <div className="warning">
              <h4>Bias Warnings:</h4>
              <ul>
                {recommendations.bias_warnings.map((warning, index) => (
                  <li key={index}>{warning}</li>
                ))}
              </ul>
            </div>
          )}
          
          <h4>Product Recommendations:</h4>
          {recommendations.products.length === 0 ? (
            <p>No product recommendations found.</p>
          ) : (
            <div className="recommendations">
              {recommendations.products.map(product => (
                <div key={product.id} className="recommendation-card">
                  <h5>{product.name || 'Unnamed Product'}</h5>
                  <p><strong>Category:</strong> {product.category || 'N/A'}</p>
                  <p><strong>Price:</strong> ${product.price?.toFixed(2) || 'N/A'}</p>
                  <p><strong>Seller Type:</strong> {product.seller_type || 'N/A'}</p>
                </div>
              ))}
            </div>
          )}
          
          <h4>Gig Recommendations:</h4>
          {recommendations.gigs.length === 0 ? (
            <p>No gig recommendations found.</p>
          ) : (
            <div className="recommendations">
              {recommendations.gigs.map(gig => (
                <div key={gig.id} className="recommendation-card">
                  <h5>{gig.title || 'Unnamed Gig'}</h5>
                  <p><strong>Category:</strong> {gig.category || 'N/A'}</p>
                  <p><strong>Budget:</strong> ${gig.budget?.toFixed(2) || 'N/A'}</p>
                  <p><strong>Skills Required:</strong> {gig.skills_required || 'N/A'}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Recommendations;