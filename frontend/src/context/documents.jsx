import React, { createContext, useContext, useEffect, useState } from "react";
import axiosInstance from "../api/axios";  // Import your custom axios instance

const DocumentsContext = createContext();

export const useDocuments = () => useContext(DocumentsContext);

export const DocumentsProvider = ({ children }) => {
  const [documents, setDocuments] = useState([]);
  const [categories, setCategories] = useState([]);
  const [category, setCategory] = useState(""); // Store the selected category
  const [filteredDocuments, setFilteredDocuments] = useState([]);

  // Fetch documents and categories on initial load
  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        // Use axiosInstance for the request
        const response = await axiosInstance.get("/documents");
        setDocuments(response.data);

        // Extract unique categories
        const uniqueCategories = [
          ...new Set(response.data.map(doc => doc.categorie)),
        ];
        setCategories(uniqueCategories);
      } catch (error) {
        console.error("Error fetching documents:", error);
      }
    };

    fetchDocuments();
  }, []);

  // Filter documents based on selected category
  useEffect(() => {
    if (category) {
      // Only filter the displayed documents
      const filtered = documents.filter(doc => doc.categorie === category);
      setFilteredDocuments(filtered);
    } else {
      setFilteredDocuments(documents); // If no category is selected, show all documents
    }
  }, [category, documents]);

  // Function to update the selected category
  const setCategoryFilter = (newCategory) => {
    setCategory(newCategory);
  };

  return (
    <DocumentsContext.Provider value={{ documents, categories, filteredDocuments, setCategoryFilter }}>
      {children}
    </DocumentsContext.Provider>
  );
};
