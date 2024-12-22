import React from "react";
import { Link } from "react-router-dom";

function TitleList({ titlesAndAuthors }) {
  return (
    <div class="rounded-md shadow-md overflow-y-auto max-h-96">
      {titlesAndAuthors?.map((document, index) => (
        <Link
          to="/read"
          state={{ title: document.title, author: document.author, id: document.id }}
          key={index}
        >
          <div
            key={index}
            class="py-2 px-4 border-b bg-cream hover:bg-yellow-200 cursor-pointer transition"
          >
            <p>{document.title}</p>
          </div>
        </Link>
      ))}
    </div>
  );
}

export default TitleList;
