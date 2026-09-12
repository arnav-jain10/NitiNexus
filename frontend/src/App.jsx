import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/home";
import Profile from "./pages/profile";
import Dashboard from "./pages/dashboard";
import SchemeDetails from "./pages/SchemeDetails";
import Partners from "./pages/Partners";
import PartnerDetails from "./pages/PartnerDetails";
import FAQ from "./pages/FAQ";
import AppShell from "./components/AppShell";
import "./App.css";
import "./light-theme.css";

function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/details" element={<Navigate to="/profile" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/scheme-details" element={<SchemeDetails />} />
          <Route path="/SchemeDetails" element={<SchemeDetails />} />
          <Route path="/partners" element={<Partners />} />
          <Route path="/partner-details" element={<PartnerDetails />} />
          <Route path="/faq" element={<FAQ />} />
          <Route path="/PartnerDetails" element={<PartnerDetails />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
}

export default App;
