import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { API_BASE } from "./config";

export default function SupplierDetails() {
  const { name } = useParams();
  const [supplier, setSupplier] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/suppliers/company/${encodeURIComponent(name)}`)
      .then((res) => res.json())
      .then((data) => setSupplier(data))
      .catch((err) => console.error(err));
  }, [name]);

  if (!supplier) {
    return <div className="page-status">Loading...</div>;
  }

  if (supplier.error) {
    return (
      <div className="container">
        <Link to="/supplier-info" className="back-link">
          ← Back to Supplier Info
        </Link>
        <h2>{supplier.error}</h2>
      </div>
    );
  }

  return (
    <div className="container">
      <Link to="/supplier-info" className="back-link">
        ← Back to Supplier Info
      </Link>

      <h1>{supplier["Supplier Name"]}</h1>

      <div className="detail-grid">
        {Object.entries(supplier).map(([key, value]) => {
          if (key === "Supplier Name" || key === "id") return null;
          if (key === "URL" && value) {
            return (
              <div key={key} className="detail-row">
                <strong>{key}:</strong>{" "}
                <a href={value} target="_blank" rel="noreferrer">
                  {value}
                </a>
              </div>
            );
          }
          return (
            <div key={key} className="detail-row">
              <strong>{key}:</strong> {String(value ?? "")}
            </div>
          );
        })}
      </div>
    </div>
  );
}
