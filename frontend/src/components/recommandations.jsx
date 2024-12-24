import React, { useState } from "react";
import Topic from "./topic";

function Recommandations({ similarDocs }) {
  // Use state to manage the number of Topics
  const [topicsCount, setTopicsCount] = useState(4);

  // Handler function for the "More" button
  const handleMoreClick = () => {
    setTopicsCount((prevCount) => prevCount + 4); // Increase the count by 4 each time
  };

  // Get the slice of similarDocs based on topicsCount
  const displayedDocs = similarDocs.slice(0, topicsCount);

  return (
    <>
      <div className="mb-10 p-5">
        <h1 className="text-2xl">Related topics</h1>
        <div className="flex-col p-5">
          <div className="flex flex-wrap">
            {displayedDocs.map((doc, index) => (
              <Topic key={index} id={doc.id} title={doc.title} similarityPourcentage={doc.similarity} />
            ))}
          </div>
          {/* Show More button only if there are more documents to show */}
          {topicsCount < similarDocs.length && (
            <div className="flex justify-center mt-4">
              <button
                className="bg-yellow-200 hover:bg-cream w-36 h-8 p-2 rounded-3xl"
                onClick={handleMoreClick}
              >
                More
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default Recommandations;
