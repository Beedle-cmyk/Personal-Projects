import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { API_BASE } from "./config";

export default function SupplierSearch() {
  const [query, setQuery] = useState("");
  const [profession, setProfession] = useState("");
  const [tag, setTag] = useState("");
  const [supplier, setSupplier] = useState("");
  const [type, setType] = useState("");

  const [results, setResults] = useState([]);
  const [tags, setTags] = useState([]);
  const [professions, setProfessions] = useState([]);
  const [allOfferings, setAllOfferings] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load filter option lists once, from the unfiltered offering set.
  useEffect(() => {
    fetch(`${API_BASE}/offerings`)
      .then((res) => res.json())
      .then(setAllOfferings)
      .catch((err) => console.error(err));

    fetch(`${API_BASE}/tags`)
      .then((res) => res.json())
      .then((rows) => setTags(rows.map((r) => r.Tag).filter(Boolean)))
      .catch((err) => console.error(err));

    fetch(`${API_BASE}/professions`)
      .then((res) => res.json())
      .then(setProfessions)
      .catch((err) => console.error(err));
  }, []);

  const supplierOptions = useMemo(
    () => [...new Set(allOfferings.map((o) => o["Supplier Name"]).filter(Boolean))].sort(),
    [allOfferings]
  );
  const typeOptions = useMemo(
    () => [...new Set(allOfferings.map((o) => o.Type).filter(Boolean))].sort(),
    [allOfferings]
  );

  const runSearch = () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (profession) params.set("profession", profession);
    if (tag) params.set("tag", tag);
    if (supplier) params.set("supplier", supplier);
    if (type) params.set("type", type);

    fetch(`${API_BASE}/offerings?${params.toString()}`)
      .then((res) => res.json())
      .then(setResults)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  // Re-run whenever a dropdown filter changes; the free-text box only
  // searches on Enter/click so we don't hit the LLM on every keystroke.
  useEffect(() => {
    runSearch();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profession, tag, supplier, type]);

  const clearFilters = () => {
    setQuery("");
    setProfession("");
    setTag("");
    setSupplier("");
    setType("");
  };

  return (
    <div className="container">
      <Link to="/" className="back-link">
        ← Home
      </Link>
      <h1>Supplier Search</h1>

      <div className="smart-search-row">
        <input
          type="text"
          placeholder='Describe what you need, e.g. "GUI library"'
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && runSearch()}
          className="search-input"
        />
        <button onClick={runSearch} className="search-button">
          Search
        </button>
      </div>

      <div className="filter-row">
        <select value={profession} onChange={(e) => setProfession(e.target.value)}>
          <option value="">All professions</option>
          {professions.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>

        <select value={tag} onChange={(e) => setTag(e.target.value)}>
          <option value="">All tags</option>
          {tags.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>

        <select value={supplier} onChange={(e) => setSupplier(e.target.value)}>
          <option value="">All suppliers</option>
          {supplierOptions.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>

        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="">All types</option>
          {typeOptions.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>

        {(profession || tag || supplier || type || query) && (
          <button onClick={clearFilters} className="clear-button">
            Clear
          </button>
        )}
      </div>

      {loading && <p className="page-status">Searching...</p>}

      {!loading && (
        <table>
          <thead>
            <tr>
              <th>Offering Name</th>
              <th>Supplier</th>
              <th>Type</th>
              <th>Tags</th>
              <th>Profession</th>
            </tr>
          </thead>
          <tbody>
            {results.map((row) => (
              <tr key={row.id}>
                <td>
                  {row.URL ? (
                    <a href={row.URL} target="_blank" rel="noreferrer">
                      {row["Offering Name"]}
                    </a>
                  ) : (
                    row["Offering Name"]
                  )}
                </td>
                <td>
                  <Link to={`/supplier-info/${encodeURIComponent(row["Supplier Name"])}`}>
                    {row["Supplier Name"]}
                  </Link>
                </td>
                <td>{row.Type}</td>
                <td>{row.Tags}</td>
                <td>{row.Profession}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!loading && results.length === 0 && (
        <p className="page-status">No offerings match your search.</p>
      )}
    </div>
  );
}
