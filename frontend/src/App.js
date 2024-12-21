import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, Link } from "react-router-dom";
import Feed from "./pages/Feed"; // Feed Component
import Profile from "./pages/Profile"; // Profile Component
import Upload from "./pages/Upload"; // Upload Component
import Register from "./pages/Register"; // Register Component
import Login from "./pages/Login"; // Login Component
import LiveStream from "./pages/LiveStream"; // Live Stream Component

const App = () => {
  const [currentTab, setCurrentTab] = useState("forYou");

  const Sidebar = () => {
    const navigate = useNavigate();

    return (
      <div className="w-32 bg-white flex flex-col items-center py-4 border-r justify-between h-screen">
        <div>
          <img src="/logo.png" alt="Logo" className="w-10 h-10 mb-4" />
          <nav className="flex flex-col gap-4">
            <button
              onClick={() => {
                setCurrentTab("forYou");
                navigate("/feed/for-you");
              }}
              className={`text-gray-800 hover:text-black text-xl ${
                currentTab === "forYou" ? "font-bold" : ""
              }`}
            >
              For You
            </button>
            <button
              onClick={() => {
                setCurrentTab("following");
                navigate("/feed/following");
              }}
              className={`text-gray-800 hover:text-black text-xl ${
                currentTab === "following" ? "font-bold" : ""
              }`}
            >
              Following
            </button>
            <button
              onClick={() => {
                setCurrentTab("podcasts");
                navigate("/feed/podcasts");
              }}
              className={`text-gray-800 hover:text-black text-xl ${
                currentTab === "podcasts" ? "font-bold" : ""
              }`}
            >
              Podcasts
            </button>
          </nav>
        </div>
        {/* Go Live Button */}
        <div className="my-4">
          <Link
            to="/live"
            className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-700 text-center text-lg"
          >
            Go Live
          </Link>
        </div>
        <div>
          <Link to="/profile" className="text-gray-800 hover:text-black text-xl mb-4 block">
            Profile
          </Link>
          <Link to="/register" className="text-gray-800 hover:text-black text-xl mb-4 block">
            Register
          </Link>
          <Link to="/login" className="text-gray-800 hover:text-black text-xl block">
            Login
          </Link>
        </div>
      </div>
    );
  };

  return (
    <Router>
      <div className="flex">
        {/* Sidebar is static and rendered on the left */}
        <Sidebar />
        {/* Main Content */}
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Navigate to="/feed/for-you" replace />} />
            <Route path="/feed/for-you" element={<Feed currentTab="forYou" />} />
            <Route path="/feed/following" element={<Feed currentTab="following" />} />
            <Route path="/feed/podcasts" element={<Feed currentTab="podcasts" />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/live" element={<LiveStream />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
