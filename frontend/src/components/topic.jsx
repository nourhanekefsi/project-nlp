import React from "react";
import { Link } from "react-router-dom";

function Topic({ id, title, similarityPourcentage }) {
  return (
    // Apply styling directly to Link element
    <Link to="/read" state={{ title: title, authoer:"",id: id }} className="w-1/3 h-fit flex text-wrap bg-cream m-0.5 hover:bg-yellow-200">
      <div className="w-full h-full flex p-2">
        <h2 className="m-auto p-2">{title}</h2>
        <div className="p-2 m-auto">{(similarityPourcentage * 100).toFixed(2)}%</div>
      </div>
    </Link>
  );
}

export default Topic;
