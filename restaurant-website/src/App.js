import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import BookingPage from './components/BookingPage';
import OnlineOrderPage from './components/OnlineOrderPage';
import './App.css';
import backgroundImage from './assets/images/background.jpg';
import image1 from './assets/images/about_restaurant_1.jpg';
import image2 from './assets/images/about_restaurant_2.jpg';

function App() {
  const [menuItems, setMenuItems] = useState([]);
  const [currentPage, setCurrentPage] = useState('home');

  useEffect(() => {
    fetch('http://localhost:3001/api/menu')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data && data.data) {
          setMenuItems(data.data);
        } else {
          console.error('Data format is incorrect:', data);
        }
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  }, []);

  const handleBookingClick = () => {
    setCurrentPage('booking');
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
  };

  if (currentPage === 'booking') {
    return <BookingPage onBack={handleBackToHome} />;
  }

  if (currentPage === 'online-order') {
    return <OnlineOrderPage onBack={handleBackToHome} />;
  }

  return (
    <div className="App">
      <Header setCurrentPage={setCurrentPage} /> {/* Pass setCurrentPage to Header */}
      <section
        className="hero"
        style={{ backgroundImage: `url(${backgroundImage})` }}
      >
        <div className="overlay"></div>
        <div className="hero-content text-center text-white">
          <h1>Enjoy Our Delicious Meal</h1>
          <p>Experience the best dining with us.</p>
          <button onClick={handleBookingClick} className="btn btn-warning">
            Book a Table
          </button>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="about-section">
        <div className="container">
          <div className="about-content">
            <div className="about-images">
              <img src={image1} alt="AI Appetite Restaurant" className="about-image about-image1" />
              <img src={image2} alt="AI Appetite Restaurant" className="about-image about-image2" />
            </div>
            <div className="about-text">
              <div className="about-title-container">
                <h2 className="about-title">About</h2>
                <h3 className="about-subtitle">AI Appetite Restaurant</h3>
              </div>
              <p>
                AI Appetite Restaurant, owned by Indonesian culinary enthusiasts, offers a unique blend of global cuisines with a touch of Indonesian flavors. Our diverse menu features dishes from around the world, all infused with the rich spices and traditional cooking methods of Indonesia, creating a truly international dining experience with a local twist.
              </p>
              <p>
                Since our establishment in 1990, we have been committed to delivering unforgettable dining experiences, combining the warmth of Indonesian hospitality with the excitement of global culinary trends.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Menu Section */}
      <section id="menu" className="menu-section">
        <div className="container">
          <h2 className="section-title">Our Menu</h2>
          <div className="menu-items">
            {menuItems.length > 0 ? (
              menuItems.map(item => (
                <div key={item.id} className="menu-item">
                  <img src={`http://localhost:3001${item.image}`} alt={item.name} className="menu-image" />
                  <h3>{item.name}</h3>
                  <p className="menu-price">{item.price}</p>
                </div>
              ))
            ) : (
              <p>No menu items available.</p>
            )}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact-section">
        <div className="container">
          <h2 className="section-title">Contact Us</h2>
          <p>If you have any questions or would like to make a reservation, feel free to reach out to us!</p>
          <p>Email: contact@aiappetiterestaurant.com</p>
          <p>Phone: +61-123-4567</p>
          <p>Address: 123 Flinders Lane, Melbourne VIC 3000, Australia</p>
        </div>
      </section>

      <main>
        {/* Additional content goes here */}
      </main>
    </div>
  );
}

export default App;
