import React from "react";
import ScorallableList from "../components/scorallableList";
import Button from "../components/button";
const { getAllCategories} = require("../documentsUtils");

export default function HomePage() {

  // Get all categories
  const categories = getAllCategories();

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
            <Button name="Upload" type="upload" />
            <Button name="Write" to="/write" />
          </div>
        </div>
      </main>

      <section className="py-32 justify-center items-center flex">
        <ScorallableList items={categories} />
      </section>
      
    </>
  );
}
