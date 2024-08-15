import React from 'react';
import Header from './Header'; // Corrected path
import './SuccessPage.css'; // Import the SuccessPage CSS

const SuccessPage = ({ onBack }) => {
  return (
    <div>
      <Header showNavLinks={false} /> {/* Show header without navigation links */}
      <div className="success-container text-center">
        <h2>Order Submitted Successfully!</h2>
        <p>Thank you for your order. We look forward to serving you at AI Appetite Restaurant.</p>
        <button onClick={onBack} className="btn btn-primary mt-3">
          Back to Main Menu
        </button>
      </div>
    </div>
  );
};

export default SuccessPage;
