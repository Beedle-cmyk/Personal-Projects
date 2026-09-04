import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Home";
import SupplierInfo from "./SupplierInfo";
import SupplierSearch from "./SupplierSearch";
import SupplierDetails from "./SupplierDetails";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/supplier-info" element={<SupplierInfo />} />
        <Route path="/supplier-info/:name" element={<SupplierDetails />} />
        <Route path="/supplier-search" element={<SupplierSearch />} />
      </Routes>
    </BrowserRouter>
  );
}
