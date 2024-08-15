import React from 'react';

const BookingPage = ({ onBack }) => {
  return (
    <div className="container text-center">
      <h2>Book a Table</h2>
      <p>Please fill out the form below to book a table at AI Appetite Restaurant.</p>
      {/* You can add your booking form here later */}
      <button onClick={onBack} className="btn btn-primary mt-3">
        Back to Main Menu
      </button>
    </div>
  );
};

export default BookingPage;
