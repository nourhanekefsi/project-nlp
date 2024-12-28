import React, { useState, useEffect } from "react";
import axiosInstance from "../api/axios";

const Visuals = ({id}) => {
  const [wordCloud, setWordCloud] = useState(null);

  useEffect(() => {
    const fetchWordCloud = async () => {
      try {
        const formData = new FormData();
        formData.append("id", id);
  
        const response = await axiosInstance.post("/wordCloud", formData, {
          headers: {
            "Content-Type": "multipart/form-data", // Ensure the correct content type
          },
          responseType: "blob", // Handle binary data
        });
  
        // Create a URL for the image blob
        const imageUrl = URL.createObjectURL(new Blob([response.data]));
        setWordCloud(imageUrl);
      } catch (error) {
        console.error("Error fetching word cloud:", error);
      }
    };
  
    fetchWordCloud();
  }, []);
  

  return (
    <div className="w-1/3 p-6">
      {wordCloud ? (
        <img src={wordCloud} alt="Word Cloud" />
      ) : (
        <p>Loading word cloud...</p>
      )}
    </div>
  );
};

export default Visuals;
