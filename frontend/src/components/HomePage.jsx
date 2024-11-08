// src/components/HomePage.jsx
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-600 to-purple-600 text-gray-50 p-4">
      <div className="bg-white/20 backdrop-blur-lg p-10 rounded-xl shadow-2xl max-w-md w-full text-center transition-transform transform hover:scale-105">
        <h1 className="text-4xl font-extrabold mb-6 leading-tight">
          Welcome to the Braille Translator
        </h1>
        <p className="text-lg mb-8">
          This is the home page. Click below to go to the dashboard.
        </p>
        <Link
          to="/dashboard"
          className="inline-block bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2 px-5 rounded-lg shadow-lg transition-all transform hover:shadow-xl hover:-translate-y-1"
        >
          Get Started
        </Link>
      </div>
    </div>
  );
};

export default HomePage;
