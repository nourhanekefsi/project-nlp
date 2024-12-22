import React, { useState } from "react";
import Topic from "./topic";

function Recommandations() {
  // Use state to manage the number of Topics
  const [topicsCount, setTopicsCount] = useState(4);

  // Handler function for the "More" button
  const handleMoreClick = () => {
    setTopicsCount((prevCount) => prevCount + 4); // Increase the count by 4 each time
  };

  return (
    <>
      <div className='mb-10 p-5'>
        <h1 className="text-2xl">Related topics</h1>
        <div className="flex-col p-5">
          <div className="flex flex-wrap">
            {[...Array(topicsCount)].map((_, index) => (
              <Topic key={index} />
            ))}
          </div>
          <div className="flex justify-center mt-4">
            <button
              className="bg-yellow-200 hover:bg-cream w-36 h-8 p-2 rounded-3xl"
              onClick={handleMoreClick}
            >
              More
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default Recommandations;
