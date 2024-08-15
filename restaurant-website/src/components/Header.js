import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';
import logo from '../assets/images/logo.png'; // Make sure the path is correct

const Header = ({ showNavLinks = true, setCurrentPage }) => {
  return (
    <header>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <a className="navbar-brand" href="#home">
            <img src={logo} alt="AI Appetite Restaurant Logo" className="logo" />
            AI Appetite
          </a>
          {showNavLinks && (
            <>
              <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
              </button>
              <div className="collapse navbar-collapse justify-content-center" id="navbarNav">
                <ul className="navbar-nav">
                  <li className="nav-item">
                    <a className="nav-link active" href="#home">Home</a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" href="#about">About</a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" href="#menu">Menu</a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" href="#contact">Contact</a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" href="#" onClick={() => setCurrentPage('online-order')}>Online Order</a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" href="#" onClick={() => setCurrentPage('ai-voice-order')}>AI Voice Order</a> {/* New NavLink */}
                  </li>
                </ul>
              </div>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}

export default Header;
