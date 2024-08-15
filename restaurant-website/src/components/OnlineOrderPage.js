import React from 'react';
import Header from './Header'; // Import the Header component
import './OnlineOrderPage.css'; // Import the OnlineOrderPage CSS

const OnlineOrderPage = ({ onBack }) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission logic here
  };

  return (
    <div>
      <Header showNavLinks={false} /> {/* Show header without navigation links */}
      <div className="online-order-container">
        <h2 className="online-order-title">Place Your Online Order</h2>
        <p>Please fill out the form below to place your order at AI Appetite Restaurant.</p>

        <form className="online-order-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input type="text" className="form-control" id="name" placeholder="Enter your name" required />
          </div>
          <div className="form-group">
            <label htmlFor="menu">Menu and Quantity:</label>
            <input type="text" className="form-control" id="menu" placeholder="Enter menu item and quantity" required />
          </div>
          <div className="form-group">
            <label htmlFor="payment-id">Payment ID:</label>
            <input type="text" className="form-control" id="payment-id" placeholder="Enter your payment ID" required />
          </div>
          <div className="form-group">
            <label htmlFor="payment-number">Payment Number:</label>
            <input type="text" className="form-control" id="payment-number" placeholder="Enter your payment number" required />
          </div>
          <div className="form-group">
            <label htmlFor="address">Address:</label>
            <input type="text" className="form-control" id="address" placeholder="Enter your address" required />
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

export default OnlineOrderPage;
