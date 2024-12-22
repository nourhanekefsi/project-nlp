import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import TitleList from "../components/titleList"; // Update path as needed
import { getTitlesAndAuthorsByCategory } from "../documentsUtils"; // Ensure correct import

function DocumentsTitles() {
  const { category } = useParams(); // Category parameter from URL
  const [titlesAndAuthors, setTitlesAndAuthors] = useState([]);

  useEffect(() => {
    // Fetch titles and authors when the category changes
    const titlesAndAuthors = getTitlesAndAuthorsByCategory(category);
    setTitlesAndAuthors(titlesAndAuthors);
  }, [category]); // Run effect when `category` changes

  return (
    <div className="max-w-lg mx-auto mt-8">
      <h1 className="text-center text-black font-bold text-2xl mb-4">
        All documents related to{" "}
        {category
          ? category.charAt(0).toUpperCase() + category.slice(1)
          : "?"}{" "}
        - {titlesAndAuthors.length}
      </h1>
      <TitleList titlesAndAuthors={titlesAndAuthors} />
    </div>
  );
}

export default DocumentsTitles;
