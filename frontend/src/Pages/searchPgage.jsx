import React, { useRef, useState } from "react";
import Recommandations from "../components/recommandations";

function SearchPgage() {
  const fileInputRef = useRef(null);

  const [value, setValue] = useState({
    content: "",
  });

  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("write"); // "write" or "upload"
  const [complete, setComplete] = useState(false);
  const handleChange = (e) => {
    const { name, value: fieldValue } = e.target;
    setValue((prev) => ({
      ...prev,
      [name]: fieldValue,
    }));
  };

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
    }
  };

  const isFormComplete = () => {
    if (mode === "upload") {
      return file;
    }
    return value.content;
  };

  const onSearch = () => {
    if (isFormComplete()) {
      console.log({
        title: value.title,
        author: value.author,
        content: value.content,
        file: mode === "upload" ? file?.name : null,
      });
      setComplete(true);
    } else {
    }
  };

  return (
    <div className="w-full flex p-10">
      <button
        className={`absolute top-6 right-20 text-white w-24 p-0.5 rounded-3xl ${
          isFormComplete()
            ? "bg-lightGreen hover:bg-green"
            : "bg-green cursor-not-allowed"
        }`}
        onClick={onSearch}
        disabled={!isFormComplete()}
      >
        Search
      </button>
      <div className="h-full w-full flex-col">
        <div className="w-full">
          <label>
            <input
              type="radio"
              name="mode"
              value="write"
              checked={mode === "write"}
              onChange={() => setMode("write")}
              className="mr-2"
            />
            Write
          </label>
          <label className="ml-4">
            <input
              type="radio"
              name="mode"
              value="upload"
              checked={mode === "upload"}
              onChange={() => setMode("upload")}
              className="mr-2"
            />
            Upload
          </label>
        </div>

        {mode === "upload" ? (
          <>
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
            <button
              className="bg-Green hover:bg-lightGreen text-white mt-4 w-24 p-0.5 rounded-3xl"
              onClick={handleUploadClick}
            >
              Upload
            </button>
            {file && (
              <span className="ml-4 text-gray-600">
                {file.name} <span className="text-sm">(Uploaded)</span>
              </span>
            )}
          </>
        ) : (
          <textarea
            name="content"
            value={value.content}
            onChange={handleChange}
            placeholder="Write your story here..."
            className="w-full p-4 text-lg rounded-lg focus:outline-none resize-none mt-4"
            rows="6"
          />
        )}
        {complete && <Recommandations />}
      </div>
    </div>
  );
}

export default SearchPgage;
