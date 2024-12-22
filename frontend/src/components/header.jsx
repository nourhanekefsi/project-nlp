import { Link } from "react-router-dom";

const Header = () => {
  
  return (
    <header className="bg-cream text-black py-4 shadow-md">
      <div className="container mx-auto px-4">
        <Link to={`/`}>
          <h1 className="text-2xl">
            <span className="text-black font-normal">Recom</span>
            <span className="text-black font-bold">Docs</span>
          </h1>
        </Link>
      </div>
    </header>
  );
};

export default Header;
