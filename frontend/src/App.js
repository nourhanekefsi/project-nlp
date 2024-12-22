import Header from "./components/header";
import DocumentsTitles from "./Pages/documentsTitles";
import HomePage from "./Pages/homePage";
import ReadPage from "./Pages/readPage";
import WritePage from "./Pages/writePage";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";


function App() {
  return (
    <div className="App">
      <Router>
        <div>
          <Header />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/documents/:category" element={<DocumentsTitles />} /> {/* Dynamic route */}
            <Route path="/read" element={<ReadPage />} />
            <Route path="/write" element={<WritePage />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
