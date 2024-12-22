import React, { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom

const ScorallableList = ({ items }) => {
  const listRef = useRef(null);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    const list = listRef.current;
    let animationFrameId;

    const startAutoScroll = () => {
      const scroll = () => {
        if (!isHovered && list) {
          list.scrollLeft += 1; // Increment for smooth scrolling
          // If the list has scrolled past the first set of items, reset to the beginning
          if (list.scrollLeft >= list.scrollWidth / 3) {
            list.scrollLeft = 0; // Reset to start once the scroll reaches 1/3 of total scroll width
          }
        }
        animationFrameId = requestAnimationFrame(scroll);
      };
      scroll();
    };

    startAutoScroll();

    return () => cancelAnimationFrame(animationFrameId);
  }, [isHovered]);

  const handleMouseEnter = () => setIsHovered(true);
  const handleMouseLeave = () => setIsHovered(false);

  const scrollLeft = () => {
    const list = listRef.current;
    if (list) {
      list.scrollLeft -= 100; // Manual scroll left
    }
  };

  const scrollRight = () => {
    const list = listRef.current;
    if (list) {
      list.scrollLeft += 100; // Manual scroll right
    }
  };

  return (
    <div
      className="relative flex items-center w-1/2 space-x-4" // Add space between buttons and list using space-x-4
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {/* Scroll left button */}
      <button
        className="bg-gray-300 p-2 z-10"
        onClick={scrollLeft}
        aria-label="Scroll Left"
      >
        &lt;
      </button>

      {/* Scrollable list */}
      <div className="overflow-hidden flex w-full" ref={listRef}>
        <div
          className="flex whitespace-nowrap"
          style={{ display: "flex", gap: "1rem" }}
        >
          {/* Duplicate items for seamless scrolling */}
          {[...items, ...items, ...items].map((item, index) => (
            <Link key={index} to={`/documents/${item.toLowerCase()}`}>
              <span
                className="inline-block px-4 text-2xl cursor-pointer font-bold hover:underline"
                style={{ whiteSpace: "nowrap" }}
              >
                {item.charAt(0).toUpperCase() + item.slice(1)}
              </span>
            </Link>
          ))}
        </div>
      </div>

      {/* Scroll right button */}
      <button
        className="bg-gray-300 p-2 z-10"
        onClick={scrollRight}
        aria-label="Scroll Right"
      >
        &gt;
      </button>
    </div>
  );
};

export default ScorallableList;
