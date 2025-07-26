import { useState } from 'react';
import { askQuestion } from '../services/api';

function Ask() {
  const [query, setQuery] = useState('');
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    // Add user query to the conversations
    const userQuery = {
      id: conversations.length + 1,
      text: query,
      sender: 'user'
    };
    
    setConversations([...conversations, userQuery]);
    setLoading(true);
    setError(null);
    
    try {
      // Send query to the API
      const response = await askQuestion(query);
      
      // Add assistant response to the conversations
      const assistantResponse = {
        id: conversations.length + 2,
        text: response.answer,
        sender: 'assistant'
      };
      
      setConversations(prevConversations => [...prevConversations, assistantResponse]);
    } catch (err) {
      console.error('Error asking question:', err);
      setError('Failed to get an answer. Please try again.');
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  return (
    <div className="container">
      <h2>Ask a Question</h2>
      <p>Ask the AI assistant any question about products, gigs, or general information</p>
      
      <div className="message-list">
        {conversations.length === 0 && (
          <div className="message assistant-message">
            <p>Hello! I'm the QLIQ AI Assistant. How can I help you today?</p>
            <p>You can ask me about:</p>
            <ul>
              <li>Product recommendations</li>
              <li>Available gigs</li>
              <li>General questions about QLIQ</li>
            </ul>
          </div>
        )}
        
        {conversations.map(conv => (
          <div 
            key={conv.id} 
            className={`message ${conv.sender === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <strong>{conv.sender === 'user' ? 'You' : 'Assistant'}:</strong> {conv.text}
          </div>
        ))}
        
        {loading && <div className="message assistant-message">Thinking...</div>}
        {error && <div className="error">{error}</div>}
      </div>
      
      <form onSubmit={handleSubmit} className="form-group">
        <div style={{ display: 'flex', gap: '1rem' }}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your question here..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !query.trim()}>
            Ask
          </button>
        </div>
      </form>
    </div>
  );
}

export default Ask;