import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

export default function SupplierDetails() {
  const { name } = useParams();
  const [supplier, setSupplier] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/suppliers/company/${encodeURIComponent(name)}`)
      .then((res) => res.json())
      .then((data) => setSupplier(data))
      .catch((err) => console.error(err));
  }, [name]);

  if (!supplier) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <Link to="/">← Back to Search</Link>

      <h1>{supplier['Supplier Name']}</h1>

      {Object.entries(supplier).map(([key, value]) => (
        <div key={key} style={{ marginBottom: '10px' }}>
          <strong>{key}:</strong> {String(value ?? '')}
        </div>
      ))}
    </div>
  );
}
