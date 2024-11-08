import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Add styles for the navbar

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          Logo
        </Link>
        <div className="navbar-links">
          <Link to="/dashboard" className="navbar-link">Dashboard</Link>
          <Link to="/" className="navbar-link">Home</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
