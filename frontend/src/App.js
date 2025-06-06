import "./App.css";
import About from "./pages/About/About";
import EligibilityTool from "./pages/EligibilityTool/EligibilityTool";
import DegreeTracker from "./pages/DegreeTracker/DegreeTracker";
import Contact from "./pages/Contact/Contact";
import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./layout/Layout";

// put our routes to the diff pages in here
function App() {
  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route
            path='/'
            element={<DegreeTracker />}
          />
          <Route
            path='/eligibility-tool'
            element={<EligibilityTool />}
          />
          <Route
            path='/about'
            element={<About />}
          />
          <Route
            path='/contact'
            element={<Contact />}
          />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
