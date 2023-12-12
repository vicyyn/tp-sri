import { useState } from "react";
import { Button, Form } from "react-bootstrap";
import { useDispatch } from "./Thunk";
import { API_PATH } from "./Consts";
import { toast } from "react-toastify";
import { dispatchSearchResult } from "./Reducer";

const SearchQueryInput = () => {
  const [query, setQuery] = useState("");
  const dispatch = useDispatch();

  const handleInputChange = (e: any) => {
    const inputValue = e.target.value;
    setQuery(inputValue);
  };

  const handleSearch = async () => {
    const formData = new FormData();
    formData.append("query", query);
    const response = await fetch(`${API_PATH}/search`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(dispatchSearchResult(data));
    } else {
      toast("An error has occured", {
        type: "error",
        autoClose: 2000,
      });
    }
  };

  return (
    <div>
      <Form.Group className="mb-3" style={{
        background: "#444"
      }}>
        <Form.Label>Query</Form.Label>
        <Form.Control style={{
        background: "#444",
        color: "#fff"
      }}
          as="textarea"
          rows={3}
          onChange={handleInputChange}
          value={query}
        />
      </Form.Group>
      <Form.Group className="mb-3 d-flex algin-items-center justify-content-end">
        <Button onClick={handleSearch} style={{
          width: "100%"
        }}>Search</Button>
      </Form.Group>
    </div>
  );
};

export default SearchQueryInput;