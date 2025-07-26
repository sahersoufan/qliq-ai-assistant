import { useState } from 'react';
import { onboardUser } from '../services/api';

function Onboarding() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    { 
      id: 1, 
      text: 'Welcome to QLIQ AI Assistant! I\'m here to help you get started. How can I assist you today?', 
      sender: 'assistant' 
    }
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!message.trim()) return;
    
    // Add user message to the chat
    const userMessage = {
      id: messages.length + 1,
      text: message,
      sender: 'user'
    };
    
    setMessages([...messages, userMessage]);
    setLoading(true);
    setError(null);
    
    try {
      // Send message to the API
      const response = await onboardUser(message);
      
      // Add assistant response to the chat
      const assistantMessage = {
        id: messages.length + 2,
        text: response.response,
        sender: 'assistant'
      };
      
      setMessages(prevMessages => [...prevMessages, assistantMessage]);
    } catch (err) {
      console.error('Error during onboarding:', err);
      setError('Failed to get a response. Please try again.');
    } finally {
      setLoading(false);
      setMessage('');
    }
  };

  return (
    <div className="container">
      <h2>Onboarding</h2>
      <p>Chat with the AI assistant to get started with QLIQ</p>
      
      <div className="message-list">
        {messages.map(msg => (
          <div 
            key={msg.id} 
            className={`message ${msg.sender === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <strong>{msg.sender === 'user' ? 'You' : 'Assistant'}:</strong> {msg.text}
          </div>
        ))}
        
        {loading && <div className="message assistant-message">Typing...</div>}
        {error && <div className="error">{error}</div>}
      </div>
      
      <form onSubmit={handleSubmit} className="form-group">
        <div style={{ display: 'flex', gap: '1rem' }}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message here..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !message.trim()}>
            Send
          </button>
        </div>
      </form>
    </div>
  );
}

export default Onboarding;