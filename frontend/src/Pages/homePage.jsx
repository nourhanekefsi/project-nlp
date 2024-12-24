import React from "react";
import ScorallableList from "../components/scorallableList";
import Button from "../components/button";
import { useDocuments } from "../context/documents";

export default function HomePage() {

  // Get all categories
  const { categories } = useDocuments();

  return (
    <>
      <main className="bg-cream text-center">
        {/* Background Text Section */}
        <div
          className="bg-cover bg-center relative h-64"
          style={{
            backgroundImage: `url('../imgs/wordCloud.jpg')`,
          }}
        >
          <div className="flex justify-center items-center absolute bottom-0 w-full space-x-80">
            <Button name="Upload" to="/upload" />
            <Button name="Search" to="/search" />
          </div>
        </div>
      </main>

      <section className="py-32 justify-center items-center flex">
        <ScorallableList items={categories} />
      </section>
      
    </>
  );
}
