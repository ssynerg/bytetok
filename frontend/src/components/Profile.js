import React, { useEffect, useState } from "react";

const Profile = () => {
  const [videos, setVideos] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const token = localStorage.getItem("token");
        const userId = 1; // Replace with dynamic user ID from auth

        const response = await fetch(`http://192.168.40.19:8000/video/profile/${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch profile data");
        }

        const data = await response.json();
        setVideos(data.videos);
        setAnalytics(data.analytics);
        setLoading(false);
      } catch (err) {
        console.error(err.message);
      }
    };

    fetchProfileData();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="flex flex-col items-center bg-white">
      <div className="w-full max-w-2xl p-4">
        {/* User Analytics */}
        <div className="border-b pb-4">
          <h1 className="text-2xl font-bold">Your Analytics</h1>
          <p>Total Videos: {analytics.total_videos}</p>
          <p>Total Views: {analytics.total_views}</p>
          <p>Total Likes: {analytics.total_likes}</p>
          <p>Total Comments: {analytics.total_comments}</p>
        </div>

        {/* User Videos */}
        <div className="mt-4">
          <h2 className="text-xl font-bold mb-4">Your Videos</h2>
          <div className="grid grid-cols-1 gap-4">
            {videos.map((video) => (
              <div key={video.id} className="border p-4 rounded shadow">
                <video
                  src={`http://192.168.40.19:8000${video.url}`}
                  controls
                  className="w-full h-64 object-cover mb-2"
                ></video>
                <h3 className="font-bold">{video.title}</h3>
                <p>{video.description}</p>
                <p>Views: {video.views}</p>
                <p>Likes: {video.likes}</p>
                <p>Comments: {video.comments}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
