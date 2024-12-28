import Header from "./components/header";
import { DocumentsProvider } from "./context/documents";
import DocumentsTitles from "./Pages/documentsTitles";
import HomePage from "./Pages/homePage";
import ReadPage from "./Pages/readPage";
import SearchPgage from "./Pages/searchPgage";
import WritePage from "./Pages/writePage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
function App() {

  return (
    <div className="App">
      <DocumentsProvider>
        {/* Wrap your app with the provider */}
        <Router>
          <div>
            <Header />
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route
                path="/documents/:category"
                element={<DocumentsTitles />}
              />
              {/* Dynamic route */}
              <Route path="/read" element={<ReadPage />} />
              <Route path="/upload" element={<WritePage />} />
              <Route path="/search" element={<SearchPgage />} />
            </Routes>
          </div>
        </Router>
      </DocumentsProvider>
    </div>
  );
}

export default App;
