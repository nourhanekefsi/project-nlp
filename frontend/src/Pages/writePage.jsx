

import React, { useState, useRef } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const WritePage = ({ upload }) => {
  const fileInputRef = useRef(null);

  const [value, setValue] = useState({
    title: "",
    author: "",
    content: "",
  });
  const [category, setCategory] = useState("");
  const [file, setFile] = useState(null);

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
    if (upload) {
      return value.title && value.author && category && file;
    }
    return value.title && value.author && value.content && category;
  };

  const onPublish = () => {
    if (isFormComplete()) {
      console.log({
        title: value.title,
        author: value.author,
        content: value.content,
        category: category,
        file: upload ? file?.name : null,
      });
      toast.success("Your document has been successfully published!");
    } else {
      toast.error("Please fill in all fields before publishing.");
    }
  };

  return (
    <div className="relative p-10">
      <ToastContainer />
      <button
        className={`absolute top-6 right-20 text-white w-24 p-0.5 rounded-3xl ${
          isFormComplete()
            ? "bg-lightGreen hover:bg-Green"
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
        {upload ? (
          <>
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
            <button
              className="bg-green-500 text-white bg-Green hover:bg-green w-24 p-0.5 rounded-3xl"
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
            className="w-full p-4 text-lg rounded-lg focus:outline-none resize-none"
            rows="6"
          />
        )}
      </div>
    </div>
  );
};

export default WritePage;
