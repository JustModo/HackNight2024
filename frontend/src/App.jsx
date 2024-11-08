import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import DashboardPage from './components/DashboardPage';
import DownloadPage from './components/DownloadPage';  // Import DownloadPage
import DemonstrationPage from './components/DemonstrationPage';  // Import DemonstrationPage
import './index.css'


function App() {
  return (
    <Router>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/download" element={<DownloadPage />} />  {/* Route for DownloadPage */}
      <Route path="/demonstration" element={<DemonstrationPage />} />  {/* Route for DemonstrationPage */}
    </Routes>
  </Router>
  )
}

export default App
