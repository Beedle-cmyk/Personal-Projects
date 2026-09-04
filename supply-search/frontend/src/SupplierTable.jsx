import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./App.css";

export default function SupplierTable() {
  const [search, setSearch] = useState("");
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/suppliers")
      .then((res) => res.json())
      .then((rows) => setData(rows))
      .catch((err) => console.error(err));
  }, []);

  const filtered = data.filter((row) =>
    Object.values(row)
      .join(" ")
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="container">
      <h1>Supplier Search</h1>

      <input
        type="text"
        placeholder="Search..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-input"
      />

      <table>
        <thead>
          <tr>
            {filtered.length > 0 &&
              Object.keys(filtered[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
          </tr>
        </thead>

        <tbody>
          {filtered.map((row, i) => (
            <tr key={i}>
              {Object.entries(row).map(([key, value]) => (
                <td key={key}>
                  {key === "Supplier Name" ? (
                    <Link to={`/supplier/${encodeURIComponent(value)}`}>
                      {value}
                    </Link>
                  ) : (
                    String(value ?? "")
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
