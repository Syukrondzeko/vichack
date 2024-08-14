import React from 'react';
import Header from './components/Header';
import './App.css';
import backgroundImage from './assets/images/background.jpg';
import image1 from './assets/images/about_restaurant_1.jpg';
import image2 from './assets/images/about_restaurant_2.jpg';

function App() {
  return (
    <div className="App">
      <Header />
      <section
        className="hero"
        style={{ backgroundImage: `url(${backgroundImage})` }}
      >
        <div className="overlay"></div>
        <div className="hero-content text-center text-white">
          <h1>Enjoy Our Delicious Meal</h1>
          <p>Experience the best dining with us.</p>
          <a href="#booking" className="btn btn-warning">Book a Table</a>
        </div>
      </section>
      
      {/* About Section */}
      <section id="about" className="about-section">
        <div className="container">
          <div className="about-content">
            <div className="about-images">
              <img src={image1} alt="VicHack Restaurant" className="about-image about-image1" />
              <img src={image2} alt="VicHack Restaurant" className="about-image about-image2" />
            </div>
            <div className="about-text">
              <div className="about-title-container">
                <h2 className="about-title">About</h2>
                <h3 className="about-subtitle">VicHack Restaurant</h3>
              </div>
              <p>
                VicHack Restaurant, owned by Indonesian culinary enthusiasts, offers a unique blend of global cuisines with a touch of Indonesian flavors. Our diverse menu features dishes from around the world, all infused with the rich spices and traditional cooking methods of Indonesia, creating a truly international dining experience with a local twist.
              </p>
              <p>
                Since our establishment in 1990, we have been committed to delivering unforgettable dining experiences, combining the warmth of Indonesian hospitality with the excitement of global culinary trends.
              </p>
            </div>
          </div>
        </div>
      </section>

      <main>
        {/* Additional content goes here */}
      </main>
    </div>
  );
}

export default App;
