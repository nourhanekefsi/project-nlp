import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
const { getAllCategories } = require("../documentsUtils");

const WritePage = () => {
  // Get all categories
  const categories = getAllCategories();

  const [value, setValue] = useState({
    title: "",
    author: "",
    content: "",
  });
  const [category, setCategory] = useState(""); // Separate state for category

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValue((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCategoryChange = (e) => {
    setCategory(e.target.value); // Dynamically update the category
  };

  const isFormComplete = () => {
    return value.title && value.author && value.content && category;
  };

  const onPublish = () => {
    if (isFormComplete()) {
      console.log({
        title: value.title,
        author: value.author,
        content: value.content,
        category: category,
      });
      toast.success("Your document has been successfully published!");
    } else {
      toast.error("Please fill in all fields before publishing.");
    }
  };

  return (
    <div className="relative p-10">
      {/* Toast Container */}
      <ToastContainer />

      {/* Publish Button */}
      <button
        className={`absolute top-6 right-20 text-white w-24 p-0.5 rounded-3xl ${
          isFormComplete()
            ? "bg-lightGreen hover:bg-Green"
            : "bg-green cursor-not-allowed"
        }`}
        onClick={onPublish}
        disabled={!isFormComplete()} // Disable button if form is incomplete
      >
        Publish
      </button>

      <div className="max-w-4xl m-auto">
        {/* Author Input */}
        <input
          type="text"
          name="author"
          value={value.author}
          onChange={handleChange}
          placeholder="Author"
          className="w-full p-4 text-lg rounded-lg focus:outline-none mb-4"
        />

        {/* Category Input (Dynamic) */}
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
            {categories.map((category) => (
              <option key={category} value={category.charAt(0).toUpperCase() + category.slice(1)}>
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </option>
            ))}
          </datalist>
        </div>

        {/* Title Input */}
        <input
          type="text"
          name="title"
          value={value.title}
          onChange={handleChange}
          placeholder="Title"
          className="w-full p-4 text-lg rounded-lg focus:outline-none mb-4"
        />

        {/* Content Textarea */}
        <textarea
          name="content"
          value={value.content}
          onChange={handleChange}
          placeholder="Write your story here..."
          className="w-full p-4 text-lg rounded-lg focus:outline-none resize-none"
          rows="6"
        />
      </div>
    </div>
  );
};

export default WritePage;
