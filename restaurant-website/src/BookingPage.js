import React from 'react';
import Header from './components/Header'; // Import the Header component

const BookingPage = ({ onBack }) => {
  return (
    <div>
      <Header showNavLinks={false} /> {/* Show header without navigation links */}
      <div className="container text-center">
        <h2>Book a Table</h2>
        <p>Please fill out the form below to book a table at AI Appetite Restaurant.</p>
        {/* You can add your booking form here later */}
        <button onClick={onBack} className="btn btn-primary mt-3">
          Back to Main Menu
        </button>
      </div>
    </div>
  );
};

export default BookingPage;
