// Import the JSON file
const allDocuments = require("./all_documents.json");

/**
 * Get all unique categories from the JSON data.
 * @returns {string[]} A list of unique categories.
 */
function getAllCategories() {
  const categories = allDocuments.map((doc) => doc.categorie);
  return [...new Set(categories)]; // Remove duplicates
}

/**
 * Get all titles, authors, and ids for a given category.
 * @param {string} category - The category to filter by.
 * @returns {{title: string, author: string, id: string}[]} A list of titles, authors, and ids for the given category.
 */
function getTitlesAndAuthorsByCategory(category) {
  return allDocuments
    .filter((doc) => doc.categorie.toLowerCase() === category.toLowerCase())
    .map((doc) => ({ title: doc.title, author: doc.author, id: doc.id }));
}


module.exports = {
  getAllCategories,
  getTitlesAndAuthorsByCategory,
};
