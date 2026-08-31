import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

const suppliers = [
  "Supplier One",
  "Supplier Two",
  "Supplier Three",
];

export default function SearchBar() {
  return (
    <Autocomplete
      options={suppliers}
      renderInput={(params) => (
        <TextField {...params} label="Search Suppliers" />
      )}
    />
  );
}