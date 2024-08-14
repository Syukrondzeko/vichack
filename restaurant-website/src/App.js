import React from 'react';
import Header from './components/Header';
import './App.css';
import backgroundImage from './assets/images/background.jpg';
import image1 from './assets/images/about_restaurant_1.jpg';
import image2 from './assets/images/about_restaurant_2.jpg';

// Sample images for menus (replace these with actual paths)
import kleponCheesecake from './assets/images/menu_1.webp';
import rendangBurger from './assets/images/menu_2.webp';
import mieGoreng from './assets/images/menu_3.webp';
import meatballSoup from './assets/images/menu_4.webp';
import ayamBakar from './assets/images/menu_5.webp';
import sambalWings from './assets/images/menu_6.webp';
import nasiUdukFish from './assets/images/menu_7.webp';
import katsuCurry from './assets/images/menu_8.webp';
import nasiCampur from './assets/images/menu_9.webp';
import balinesePizza from './assets/images/menu_10.webp';

const menuItems = [
  { id: 1, image: kleponCheesecake, name: "Klepon Cheesecake", price: "$6.99", quantity: "1 slice" },
  { id: 2, image: rendangBurger, name: "Rendang Beef Burgers", price: "$12.99", quantity: "1 burger" },
  { id: 3, image: mieGoreng, name: "Mie Goreng Stir-Fry", price: "$9.99", quantity: "1 bowl" },
  { id: 4, image: meatballSoup, name: "Indonesian Meatball Soup", price: "$7.99", quantity: "1 bowl" },
  { id: 5, image: ayamBakar, name: "Ayam Bakar Teriyaki", price: "$11.99", quantity: "2 pieces" },
  { id: 6, image: sambalWings, name: "Sambal Chicken Wings", price: "$8.99", quantity: "6 pieces" },
  { id: 7, image: nasiUdukFish, name: "Nasi Uduk with Grilled Fish", price: "$10.99", quantity: "1 plate" },
  { id: 8, image: katsuCurry, name: "Katsu Curry with Nasi", price: "$13.99", quantity: "1 plate" },
  { id: 9, image: nasiCampur, name: "Nasi Campur Bowl", price: "$9.99", quantity: "1 bowl" },
  { id: 10, image: balinesePizza, name: "Balinese Spiced Veggie Pizza", price: "$14.99", quantity: "1 pizza" },
];

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

      {/* Menu Section */}
      <section id="menu" className="menu-section">
              <div className="container">
                <h2 className="section-title">Our Menu</h2>
                <div className="menu-items">
                  {menuItems.map(item => (
                    <div key={item.id} className="menu-item">
                      <img src={item.image} alt={item.name} className="menu-image" />
                      <h3>{item.name}</h3>
                      <p className="menu-price">{item.price}</p>
                      <p className="menu-quantity">{item.quantity}</p>
                    </div>
                  ))}
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
