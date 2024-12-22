import React, { useRef } from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom

function Button({ name, to, type }) {
  const fileInputRef = useRef(null);

  const handleClick = () => {
    if (type === "upload") {
      // Trigger the file input click when the button is clicked
      if (fileInputRef.current) {
        fileInputRef.current.click();
      }
    }
    // Additional logic for other types (e.g., navigation)
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Handle file upload logic here
      console.log("File selected: ", file.name);
    }
  };

  return (
    <div>
      {type === "upload" ? (
        // If the button type is "upload", it triggers a file input
        <button
          onClick={handleClick}
          className="hover:bg-yellow-200 py-2 px-6 text-black font-bold rounded-3xl shadow-lg bg-cream"
          style={{
            transform: "translateY(50%)",
            width: "200px", // Set fixed width
            height: "50px", // Set fixed height
          }}
        >
          {name}
        </button>
      ) : (
        // If the button is not for upload, use a Link for navigation
        <Link to={to}>
          <button
            className="hover:bg-yellow-200  py-2 px-6 text-black font-bold rounded-3xl shadow-lg bg-cream"
            style={{
              transform: "translateY(50%)",
              width: "200px", // Set fixed width
              height: "50px", // Set fixed height
            }}
          >
            {name}
          </button>
        </Link>
      )}

      {/* Hidden file input for file upload */}
      {type === "upload" && (
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: "none" }} // Hide the input element
        />
      )}
    </div>
  );
}

export default Button;
