import React, { useState, useRef } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import axios from "axios"; // Import axios
import axiosInstance from "../api/axios";

const WritePage = () => {
  const fileInputRef = useRef(null);

  const [value, setValue] = useState({
    title: "",
    author: "",
    content: "",
  });
  const [category, setCategory] = useState("");
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("write"); // "write" or "upload"

  const handleChange = (e) => {
    const { name, value: fieldValue } = e.target;
    setValue((prev) => ({
      ...prev,
      [name]: fieldValue,
    }));
  };

  const handleCategoryChange = (e) => {
    setCategory(e.target.value);
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

  const isFormComplete = () => {
    if (mode === "upload") {
      return value.title && value.author && category && file;
    }
    return value.title && value.author && value.content && category;
  };

  const onPublish = async () => {
    if (isFormComplete()) {
      const formData = new FormData();
      formData.append("title", value.title);
      formData.append("author", value.author);
      formData.append("category", category.toLowerCase());
      if (mode === "upload" && file) {
        formData.append("file", file);
      } else {
        formData.append("content", value.content);
      }
      console.log(value.title ,value.author ,value.content , category, file);
      try {
        const response = await axiosInstance.post("/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data", // Ensure the content type is set correctly for file uploads
          },
        });

        if (response.status === 200) {
          toast.success("Your document has been successfully submitted!");
        } else {
          toast.error("Error: Unable to submit the document.");
        }
      } catch (error) {
        toast.error("An error occurred while submitting your post.");
        console.error("Error:", error);
      }
    } else {
      toast.error("Please fill in all fields before submitting.");
    }
  };

  return (
    <div className="relative p-10">
      <ToastContainer />
      <button
        className={`absolute top-6 right-20 text-white w-24 p-0.5 rounded-3xl ${
          isFormComplete()
            ? "bg-lightGreen hover:bg-green"
            : "bg-green cursor-not-allowed"
        }`}
        onClick={onPublish}
        disabled={!isFormComplete()}
      >
        Publish
      </button>

      <div className="max-w-4xl m-auto">
        <input
          type="text"
          name="author"
          value={value.author}
          onChange={handleChange}
          placeholder="Author"
          className="w-full p-4 text-lg rounded-lg focus:outline-none mb-4"
        />
        <div className="mb-4">
          <input
            type="text"
            value={category}
            onChange={handleCategoryChange}
            list="category-options"
            placeholder="Select or write a new category"
            className="w-full p-4 text-lg rounded-lg focus:outline-none"
          />
          <datalist id="category-options">
            <option value="Technology" />
            <option value="Science" />
            <option value="Health" />
          </datalist>
        </div>
        <input
          type="text"
          name="title"
          value={value.title}
          onChange={handleChange}
          placeholder="Title"
          className="w-full p-4 text-lg rounded-lg focus:outline-none mb-4"
        />
        <div className="mb-4">
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
            value={value.content}
            onChange={handleChange}
            placeholder="Write your story here..."
            className="w-full h-fit p-4 text-lg rounded-lg focus:outline-none resize-none mt-4"
            rows="6"
          />
        )}
      </div>
    </div>
  );
};

export default WritePage;
