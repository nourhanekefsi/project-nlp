import React, { useRef, useState } from "react";
import Recommandations from "../components/recommandations";
import axiosInstance from "../api/axios";

function SearchPgage() {
  const fileInputRef = useRef(null);
  const [content, setContent] = useState("");
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("write"); // "write" or "upload"
  const [complete, setComplete] = useState(false);
  const [similarDocs, setSimilarDocs] = useState([]);

  const handleChange = (e) => {
    const { value } = e.target;
    setContent(value);
  };

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
    }
  };

  // Updated function to validate if the form is complete
  const isFormComplete = () => {
    if (mode === "upload") {
      return file; // File must be uploaded
    }
    return content.trim() !== ""; // Content must be provided for 'write' mode
  };

  const onSearch = () => {
    if (isFormComplete()) {
      const formData = new FormData();

      // Check if content (text) is provided
      if (content.trim()) {
        formData.append('text', content);  // Ensure key matches the backend
      }

      // Check if a file (PDF) is uploaded
      if (mode === "upload" && file) {
        formData.append('file', file); // Append the file object directly
      }

      // If neither content nor file is provided, return early or show an error
      if (!content.trim() && (!file || mode !== "upload")) {
        console.log("No content or file provided");
        return;
      }

      // Send the POST request to the server with FormData
      axiosInstance
        .post("/search", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          // Handle the response, for example, display similar documents
          console.log("Similar documents:", response.data.similar_documents);
          setSimilarDocs(response.data);
          setComplete(true); // Mark as complete if the request was successful
        })
        .catch((error) => {
          // Handle any errors
          console.error("Error fetching similar documents:", error);
        });
    } else {
      console.log("Form is incomplete");
    }
  };

  return (
    <div className="w-full flex p-10">
      <button
        className={`absolute top-6 right-20 text-white w-24 p-0.5 rounded-3xl ${
          isFormComplete()
            ? "bg-lightGreen hover:bg-green"
            : "bg-green cursor-not-allowed"
        }`}
        onClick={onSearch}
        disabled={!isFormComplete()}
      >
        Search
      </button>
      <div className="h-full w-full flex-col">
        <div className="w-full">
          <label>
            <input
              type="radio"
              name="mode"
              value="write"
              checked={mode === "write"}
              onChange={() => setMode("write")}
              className="mr-2"
            />
            Write
          </label>
          <label className="ml-4">
            <input
              type="radio"
              name="mode"
              value="upload"
              checked={mode === "upload"}
              onChange={() => setMode("upload")}
              className="mr-2"
            />
            Upload
          </label>
        </div>

        {mode === "upload" ? (
          <>
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
            <button
              className="bg-Green hover:bg-lightGreen text-white mt-4 w-24 p-0.5 rounded-3xl"
              onClick={handleUploadClick}
            >
              Upload
            </button>
            {file && (
              <span className="ml-4 text-gray-600">
                {file.name} <span className="text-sm">(Uploaded)</span>
              </span>
            )}
          </>
        ) : (
          <textarea
            name="content"
            value={content}
            onChange={handleChange}
            placeholder="Write your story here..."
            className="w-full p-4 text-lg rounded-lg focus:outline-none resize-none mt-4"
            rows="6"
          />
        )}
        {complete && <Recommandations similarDocs={similarDocs.similar_documents} />}
      </div>
    </div>
  );
}

export default SearchPgage;
