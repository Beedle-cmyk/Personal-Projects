import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { API_BASE } from "./config";

export default function Home() {
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/meta/last-updated`)
      .then((res) => res.json())
      .then((data) => setLastUpdated(data.last_updated))
      .catch(() => setLastUpdated(null));
  }, []);

  return (
    <div className="home">
      {lastUpdated && <div className="last-updated">Last updated: {lastUpdated}</div>}

      <h1>Supply Catalog</h1>
      <p className="home-subtitle">Choose where you'd like to start.</p>

      <div className="home-choices">
        <Link to="/supplier-search" className="home-card">
          <h2>Supplier Search</h2>
          <p>
            Find products and services by profession, tag, keyword, or a
            plain-language description of what you need.
          </p>
        </Link>

        <Link to="/supplier-info" className="home-card">
          <h2>Supplier Info</h2>
          <p>
            Browse and search the full supplier directory - contacts,
            addresses, tier level, and certification status.
          </p>
        </Link>
      </div>
    </div>
  );
}
