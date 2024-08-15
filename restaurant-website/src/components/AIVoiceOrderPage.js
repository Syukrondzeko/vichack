import React from 'react';
import Header from './Header';
import './AIVoiceOrderPage.css'; // Create this CSS file for any specific styles

const AIVoiceOrderPage = ({ onBack }) => {
  return (
    <div>
      <Header showNavLinks={false} /> {/* Show header without navigation links */}
      <div className="ai-voice-order-container text-center">
        <h2>AI Voice Order</h2>
        <p>This feature is coming soon. Please check back later.</p>
        <button onClick={onBack} className="btn btn-primary mt-3">
          Back to Main Menu
        </button>
      </div>
    </div>
  );
};

export default AIVoiceOrderPage;
