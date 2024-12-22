import React from "react";
import Visuals from "../components/visuals";
import Recommandations from "../components/recommandations";
import { useLocation } from "react-router-dom";

function ReadPage() {
  const location = useLocation();
  const { title, author, id } = location.state || {}; // Safely access state
  // send id to back to retreive content
  return (
    <>
      <div className=" p-10 w-full flex-col">
        <div className="flex flex-row-reverse">
          <Visuals />
          <div className="w-2/3">
            <h1 className="text-2xl font-bold">
              {title || "No Title Provided"}
            </h1>
            <h3 className="p-1 font-bold">By : {author || "Unknown Author"}</h3>
            <p className="p-3 leading-relaxed ">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit
              amet nulla auctor, vestibulum magna sed, convallis ex. Cras
              ultricies ligula sed magna dictum porta. Lorem ipsum dolor sit
              amet, consectetur adipiscing elit. Sed sit amet nulla auctor,
              vestibulum magna sed, convallis ex. Cras ultricies ligula sed
              magna dictum porta. Lorem ipsum dolor sit amet, consectetur
              adipiscing elit. Sed sit amet nulla auctor, vestibulum magna sed,
              convallis ex. Cras ultricies ligula sed magna dictum porta. Lorem
              ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet
              nulla auctor, vestibulum magna sed, convallis ex. Cras ultricies
              ligula sed magna dictum porta. Lorem ipsum dolor sit amet,
              consectetur adipiscing elit. Sed sit amet nulla auctor, vestibulum
              magna sed, convallis ex. Cras ultricies ligula sed magna dictum
              porta. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
              Sed sit amet nulla auctor, vestibulum magna sed, convallis ex.
              Cras ultricies ligula sed magna dictum porta. Lorem ipsum dolor
              sit amet, consectetur adipiscing elit. Sed sit amet nulla auctor,
              vestibulum magna sed, convallis ex. Cras ultricies ligula sed
              magna dictum porta. Lorem ipsum dolor sit amet, consectetur
              adipiscing elit. Sed sit amet nulla auctor, vestibulum magna sed,
              convallis ex. Cras ultricies ligula sed magna dictum porta,rta.
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit
              amet nulla auctor, vestibulum magna sed, convallis ex. Cras
              ultricies ligula sed magna dictum porta. Lorem ipsum dolor sit
              amet, consectetur adipiscing elit. Sed sit amet nulla auctor,
              vestibulum magna sed, convallis ex. Cras ultricies ligula sed
              magna dictum porta. Lorem ipsum dolor sit amet, consectetur
              adipiscing elit. Sed sit amet nulla auctor, vestibulum magna sed,
              convallis ex. Cras ultricies ligula sed magna dictum porta. Lorem
              ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet
              nulla auctor, vestibulum magna sed, convallis ex. Cras ultricies
              ligula sed magna dictum porta.
            </p>
          </div>
        </div>
        <Recommandations />

      </div>
    </>
  );
}

export default ReadPage;
