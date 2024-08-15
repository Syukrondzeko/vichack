import React from 'react';
import Header from './components/Header'; // Import the Header component
import './BookingPage.css'; // Import the BookingPage CSS

const BookingPage = ({ onBack }) => {
  return (
    <div>
      <Header showNavLinks={false} /> {/* Show header without navigation links */}
      <div className="booking-container">
        <h2 className="booking-title">Book a Table</h2>
        <p>Please fill out the form below to book a table at AI Appetite Restaurant.</p>

        <form className="booking-form">
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input type="text" className="form-control" id="name" placeholder="Enter your name" required />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input type="email" className="form-control" id="email" placeholder="Enter your email" required />
          </div>
          <div className="form-group">
            <label htmlFor="phone">Phone:</label>
            <input type="tel" className="form-control" id="phone" placeholder="Enter your phone number" required />
          </div>
          <div className="form-group">
            <label htmlFor="date">Date:</label>
            <input type="date" className="form-control" id="date" required />
          </div>
          <div className="form-group">
            <label htmlFor="time">Time:</label>
            <input type="text" className="form-control" id="time" placeholder="12:30 AM" required />
          </div>
          <div className="form-group">
            <label htmlFor="guests">Number of Guests:</label>
            <input type="number" className="form-control" id="guests" min="1" max="20" placeholder="Enter number of guests" required />
          </div>

          <div className="btn-container">
            <button type="submit" className="btn btn-success mr-2">Submit Order</button>
            <button type="button" className="btn btn-danger ml-2" onClick={onBack}>Cancel Order</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default BookingPage;
