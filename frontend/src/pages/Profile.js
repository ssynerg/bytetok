import React, { useEffect, useState } from "react";

const Profile = () => {
  const [user, setUser] = useState(null); // User information
  const [videos, setVideos] = useState([]); // User's videos
  const [likedVideos, setLikedVideos] = useState([]); // User's liked videos
  const [activeTab, setActiveTab] = useState("videos"); // Active tab: 'videos' or 'liked'
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state

  // Fetch profile data from the backend
  const fetchProfileData = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("You must be logged in to view your profile.");
      return;
    }

    try {
      setLoading(true);
      const response = await fetch("http://192.168.40.19:8000/profile", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch profile data");
      }

      const data = await response.json();
      setUser(data.user); // Assuming the backend sends user details
      setVideos(data.videos || []);
      setLikedVideos(data.likedVideos || []); // Assuming liked videos are sent separately
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfileData();
  }, []);

  if (loading) {
    return <p className="text-center text-gray-500">Loading...</p>;
  }

  if (error) {
    return <p className="text-center text-red-500">{error}</p>;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center">
      {/* Profile Header */}
      <div className="w-full max-w-4xl bg-white shadow p-4 mb-4">
        {user ? (
          <div className="flex flex-col items-center">
            <div className="rounded-full bg-gray-300 w-24 h-24 flex items-center justify-center text-3xl font-bold text-white">
              {user.username.charAt(0).toUpperCase()}
            </div>
            <h2 className="text-2xl font-bold mt-2">{user.username}</h2>
            <p className="text-gray-500">{user.email}</p>

            {/* Stats */}
            <div className="flex justify-around w-full max-w-md mt-4">
              <div className="text-center">
                <p className="text-xl font-bold">{videos.length}</p>
                <p className="text-gray-500">Videos</p>
              </div>
              <div className="text-center">
                <p className="text-xl font-bold">{user.followersCount || 0}</p>
                <p className="text-gray-500">Followers</p>
              </div>
              <div className="text-center">
                <p className="text-xl font-bold">{user.followingCount || 0}</p>
                <p className="text-gray-500">Following</p>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-gray-500">User not found</p>
        )}
      </div>

      {/* Tabs */}
      <div className="w-full max-w-4xl bg-white shadow p-2 mb-4">
        <div className="flex justify-around">
          <button
            onClick={() => setActiveTab("videos")}
            className={`w-1/2 py-2 text-center ${
              activeTab === "videos" ? "border-b-2 border-black font-bold" : "text-gray-500"
            }`}
          >
            Videos
          </button>
          <button
            onClick={() => setActiveTab("liked")}
            className={`w-1/2 py-2 text-center ${
              activeTab === "liked" ? "border-b-2 border-black font-bold" : "text-gray-500"
            }`}
          >
            Liked
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="w-full max-w-4xl">
        {activeTab === "videos" && videos.length > 0 ? (
          <div className="grid grid-cols-3 gap-4">
            {videos.map((video) => (
              <div key={video.id} className="relative">
                <video
                  controls
                  src={`http://192.168.40.19:8000${video.url}`}
                  className="w-full h-full object-cover"
                />
                <p className="absolute bottom-0 left-0 bg-black text-white text-sm px-2 py-1">
                  {video.title}
                </p>
              </div>
            ))}
          </div>
        ) : activeTab === "liked" && likedVideos.length > 0 ? (
          <div className="grid grid-cols-3 gap-4">
            {likedVideos.map((video) => (
              <div key={video.id} className="relative">
                <video
                  controls
                  src={`http://192.168.40.19:8000${video.url}`}
                  className="w-full h-full object-cover"
                />
                <p className="absolute bottom-0 left-0 bg-black text-white text-sm px-2 py-1">
                  {video.title}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center text-gray-500">
            {activeTab === "videos" ? "No videos to display." : "No liked videos to display."}
          </p>
        )}
      </div>
    </div>
  );
};

export default Profile;
