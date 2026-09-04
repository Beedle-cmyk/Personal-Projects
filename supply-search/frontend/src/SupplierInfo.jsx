import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { API_BASE } from "./config";

export default function SupplierInfo() {
  const [search, setSearch] = useState("");
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/suppliers`)
      .then((res) => res.json())
      .then((rows) => setData(rows))
      .catch((err) => console.error(err));
  }, []);

  const filtered = data.filter((row) =>
    Object.values(row).join(" ").toLowerCase().includes(search.toLowerCase())
  );

  // "id" is an internal key from the converter, not useful to show
  const visibleColumns = filtered.length > 0
    ? Object.keys(filtered[0]).filter((k) => k !== "id")
    : [];

  return (
    <div className="container">
      <Link to="/" className="back-link">
        ← Home
      </Link>
      <h1>Supplier Info</h1>

      <input
        type="text"
        placeholder="Search suppliers..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-input"
      />

      <table>
        <thead>
          <tr>
            {visibleColumns.map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {filtered.map((row, i) => (
            <tr key={i}>
              {visibleColumns.map((key) => (
                <td key={key}>
                  {key === "Supplier Name" ? (
                    <Link to={`/supplier-info/${encodeURIComponent(row[key])}`}>
                      {row[key]}
                    </Link>
                  ) : (
                    String(row[key] ?? "")
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
