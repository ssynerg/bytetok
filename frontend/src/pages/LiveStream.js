import React, { useState, useRef, useEffect } from "react";

const LiveStream = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isLive, setIsLive] = useState(false);
  const videoRef = useRef(null);
  const [stream, setStream] = useState(null);

  // Access the user's camera
  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (error) {
      console.error("Error accessing camera:", error);
    }
  };

  // Stop the camera
  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
    setStream(null);
  };

  const handleStartStream = async () => {
    try {
      const response = await fetch("http://192.168.40.19:8000/live-stream/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ title, description }),
      });
      if (!response.ok) {
        throw new Error("Failed to start live stream");
      }
      const data = await response.json();
      console.log("Live stream started:", data);
      setIsLive(true);
      startCamera();
    } catch (error) {
      console.error("Error starting live stream:", error);
    }
  };

  const handleStopStream = async () => {
    try {
      const response = await fetch("http://192.168.40.19:8000/live-stream/stop", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (!response.ok) {
        throw new Error("Failed to stop live stream");
      }
      setIsLive(false);
      stopCamera();
    } catch (error) {
      console.error("Error stopping live stream:", error);
    }
  };

  useEffect(() => {
    return () => {
      // Stop the camera if the component unmounts
      stopCamera();
    };
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Live Stream</h1>
      {!isLive ? (
        <div>
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="mb-2 p-2 border"
          />
          <textarea
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="mb-2 p-2 border w-full"
          ></textarea>
          <button onClick={handleStartStream} className="bg-blue-500 text-white px-4 py-2">
            Start Live Stream
          </button>
        </div>
      ) : (
        <div>
          <video
            ref={videoRef}
            autoPlay
            muted
            className="w-full h-64 bg-black"
          ></video>
          <button onClick={handleStopStream} className="bg-red-500 text-white px-4 py-2 mt-4">
            Stop Live Stream
          </button>
        </div>
      )}
    </div>
  );
};

export default LiveStream;
