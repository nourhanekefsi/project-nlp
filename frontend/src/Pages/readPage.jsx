import React, { useEffect, useState } from "react";
import Visuals from "../components/visuals";
import Recommandations from "../components/recommandations";
import { useLocation } from "react-router-dom";
import axiosInstance from "../api/axios";

function ReadPage() {
  const location = useLocation();
  const { id } = location.state || {}; // Safely access state
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Send id to backend to retrieve content
  useEffect(() => {
    const fetchDocument = async () => {
      try {
        setLoading(true);
        const response = await axiosInstance.get(`/document/${id}/details`);
        setDocument(response.data);
        console.log("Document", response.data);
      } catch (err) {
        setError("Error fetching document: " + err.message);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchDocument();
    }
  }, [id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }


  return (
    <>
      {document ? (
        <div className="p-10 w-full flex-col">
          <div className="flex flex-row-reverse">
            <Visuals id={id}/>
            <div className="w-2/3">
              <h1 className="text-2xl font-bold">
                {document.document.title || "No Title Provided"}
              </h1>
              <h3 className="p-1 font-bold">
                By: {document.document.author || "No Author Provided"}
              </h3>
              <a
                href={document.document.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-lightGreen underline"
              >
                Direct link to the website
              </a>
              <div className="flex justify-center items-center min-h-screen">
                <iframe
                  src={document.document.link}
                  title={document.document.title}
                  className="w-full h-[1000px] border-none"
                  loading="lazy"
                ></iframe>
              </div>
            </div>
          </div>
          <Recommandations similarDocs={document.similar_documents} />
        </div>
      ) : (
        <div>No content found</div>
      )}
    </>
  );
}

export default ReadPage;
