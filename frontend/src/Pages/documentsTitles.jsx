import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import TitleList from "../components/titleList"; // Update path as needed
import { useDocuments } from "../context/documents";

function DocumentsTitles() {
  const { category } = useParams(); // Category parameter from URL
  const { filteredDocuments, setCategoryFilter } = useDocuments();
  console.log("filteredDocuments", filteredDocuments)
  useEffect(() => {
    // Fetch titles and authors when the category changes
    setCategoryFilter(category); // Update context with the new category
  }, [category]); // Run effect when `category` changes

  return (
    <div className="max-w-lg mx-auto mt-8">
      <h1 className="text-center text-black font-bold text-2xl mb-4">
        All documents related to{" "}
        {category
          ? category.charAt(0).toUpperCase() + category.slice(1)
          : "?"}{" "}
        - {filteredDocuments.length}
      </h1>
      <TitleList titlesAndAuthors={filteredDocuments} />
    </div>
  );
}

export default DocumentsTitles;
