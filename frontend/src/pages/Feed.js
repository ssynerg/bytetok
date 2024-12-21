import React, { useEffect, useState, useRef } from "react";

const Feed = ({ currentTab }) => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const videoRefs = useRef([]);

  const fetchVideos = async () => {
    try {
      setLoading(true);
      const skip = videos.length;
      const limit = 5;

      const endpoint = `/feed/${currentTab === "forYou" ? "for-you" : currentTab}`;
      const token = localStorage.getItem("token");

      const headers =
        currentTab === "following"
          ? {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            }
          : {};

      console.log(`Fetching: http://192.168.40.19:8000/video${endpoint}?skip=${skip}&limit=${limit}`);

      const response = await fetch(
        `http://192.168.40.19:8000/video${endpoint}?skip=${skip}&limit=${limit}`,
        {
          method: "GET",
          headers,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch videos");
      }

      const data = await response.json();
      if (data.videos.length === 0) {
        setHasMore(false);
      } else {
        setVideos((prev) => [...prev, ...data.videos]);
      }
    } catch (error) {
      console.error("Error fetching video feed:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setVideos([]);
    setHasMore(true);
    fetchVideos();
  }, [currentTab]);

  // Autoplay videos in the viewport
  useEffect(() => {
    const handleObserver = (entries) => {
      entries.forEach((entry) => {
        const video = entry.target;
        if (entry.isIntersecting) {
          video.play();
        } else {
          video.pause();
        }
      });
    };

    const observer = new IntersectionObserver(handleObserver, { threshold: 0.75 });

    videoRefs.current.forEach((video) => {
      if (video) observer.observe(video);
    });

    return () => observer.disconnect();
  }, [videos]);

  return (
    <div className="flex-1 overflow-y-scroll snap-y snap-mandatory relative">
      {videos.map((video, index) => (
        <div key={video.id} className="relative flex justify-center items-center h-screen snap-center">
          <video
            ref={(el) => (videoRefs.current[index] = el)}
            muted
            loop
            playsInline
            src={`http://192.168.40.19:8000${video.url}`}
            className="w-full h-full object-cover"
          ></video>
        </div>
      ))}
      {loading && <p className="text-center text-gray-500">Loading more videos...</p>}
      {!hasMore && <p className="text-center text-gray-500">No more videos to display.</p>}
    </div>
  );
};

export default Feed;
