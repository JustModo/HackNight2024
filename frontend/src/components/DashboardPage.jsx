// src/components/DashboardPage.jsx
import { Link } from "react-router-dom";
import "../styles/DashboardPage.css";

const DashboardPage = () => {
  return (
    <div className="dashboard p-5 w-screen h-screen flex justify-center items-center flex-col">
      <h1 className="text-3xl text-indigo-700 font-bold">Dashboard</h1>
      <div className="dashboard-buttons">
        <Link to="/download" className="dashboard-button hover:scale-105">
          Transcript Extension
        </Link>
        <Link to="/demonstration" className="dashboard-button hover:scale-105">
          Live Braille Translator
        </Link>
      </div>
    </div>
  );
};

export default DashboardPage;
