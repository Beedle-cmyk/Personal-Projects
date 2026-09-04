import { BrowserRouter, Routes, Route } from "react-router-dom";
import SupplierTable from "./SupplierTable";
import SupplierDetails from "./SupplierDetails";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SupplierTable />} />
        <Route path="/supplier/:name" element={<SupplierDetails />} />
      </Routes>
    </BrowserRouter>
  );
}
