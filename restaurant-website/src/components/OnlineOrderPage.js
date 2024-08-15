import React, { useState, useEffect } from 'react';
import Header from './Header';
import SuccessPage from './SuccessPage';
import './OnlineOrderPage.css';

const OnlineOrderPage = ({ onBack }) => {
  const [menuItems, setMenuItems] = useState([]);
  const [orderItems, setOrderItems] = useState([{ menuItem: '', quantity: '' }]);
  const [paymentType, setPaymentType] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  useEffect(() => {
    fetch('http://localhost:3001/api/menu')
      .then(response => response.json())
      .then(data => setMenuItems(data.data))
      .catch(error => console.error('Error fetching menu items:', error));
  }, []);

  const handleAddItem = () => {
    setOrderItems([...orderItems, { menuItem: '', quantity: '' }]);
  };

  const handleRemoveItem = (index) => {
    const newOrderItems = [...orderItems];
    newOrderItems.splice(index, 1);
    setOrderItems(newOrderItems);
  };

  const handleMenuItemChange = (index, value) => {
    const newOrderItems = [...orderItems];
    newOrderItems[index].menuItem = value;
    setOrderItems(newOrderItems);
  };

  const handleQuantityChange = (index, value) => {
    const newOrderItems = [...orderItems];
    newOrderItems[index].quantity = value;
    setOrderItems(newOrderItems);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setIsSubmitted(true);
  };

  if (isSubmitted) {
    return <SuccessPage onBack={onBack} />;
  }

  return (
    <div>
      <Header showNavLinks={false} />
      <div className="online-order-container">
        <h2 className="online-order-title">Place Your Online Order</h2>
        <p>Please fill out the form below to place your order at AI Appetite Restaurant.</p>

        <form className="online-order-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input type="text" className="form-control" id="name" placeholder="Enter your name" required />
          </div>

          {orderItems.map((item, index) => (
            <div key={index} className="order-item-group">
              <div className="form-group">
                <label htmlFor={`menu-${index}`}>Menu:</label>
                <select
                  id={`menu-${index}`}
                  className="form-control"
                  value={item.menuItem}
                  onChange={(e) => handleMenuItemChange(index, e.target.value)}
                  required
                >
                  <option value="" disabled>Select a menu item</option>
                  {menuItems.map((menuItem) => (
                    <option key={menuItem.id} value={menuItem.name}>
                      {menuItem.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label htmlFor={`quantity-${index}`}>Quantity:</label>
                <input
                  type="number"
                  className="form-control"
                  id={`quantity-${index}`}
                  value={item.quantity}
                  onChange={(e) => handleQuantityChange(index, e.target.value)}
                  placeholder="Enter quantity"
                  required
                />
              </div>
              <div className="btn-container-small">
                <button type="button" className="btn btn-primary btn-sm mr-2" onClick={handleAddItem}>
                  Add Menu
                </button>
                <button type="button" className="btn btn-danger btn-sm" onClick={() => handleRemoveItem(index)}>
                  Remove Menu
                </button>
              </div>
            </div>
          ))}

          <div className="form-group">
            <label htmlFor="payment-type">Payment Type:</label>
            <select
              id="payment-type"
              className="form-control"
              value={paymentType}
              onChange={(e) => setPaymentType(e.target.value)}
              required
            >
              <option value="" disabled>Select a payment type</option>
              <option value="Credit Card">Credit Card</option>
              <option value="Debit Card">Debit Card</option>
              <option value="Paypal">Paypal</option>
            </select>
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
