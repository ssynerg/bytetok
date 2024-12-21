import React, { useState } from "react";

const Upload = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!selectedFile) {
      setError("Please select a file!");
      return;
    }

    const formData = new FormData();
    formData.append("title", title); // Attach title
    formData.append("description", description); // Attach description
    formData.append("file", selectedFile); // Attach file

    const token = localStorage.getItem("token");

    if (!token) {
      setError("You must be logged in to upload videos.");
      return;
    }

    try {
      const response = await fetch("http://192.168.40.19:8000/video/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`, // Include token in headers
        },
        body: formData, // Send FormData as the body
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Upload failed");
      }

      const responseData = await response.json();
      setSuccess("Video uploaded successfully!");
      console.log("Response from backend:", responseData);
    } catch (err) {
      setError(err.message || "An error occurred during upload.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="max-w-md mx-auto p-4 border rounded shadow bg-white"
      >
        <h2 className="text-2xl font-bold mb-4">Upload Video</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        {success && <p className="text-green-500 mb-4">{success}</p>}
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="block w-full mb-4 p-2 border rounded"
          required
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="block w-full mb-4 p-2 border rounded"
          required
        ></textarea>
        <input
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          className="block w-full mb-4 p-2 border"
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-700"
        >
          Upload
        </button>
      </form>
    </div>
  );
};

export default Upload;
