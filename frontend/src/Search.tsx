import React, { useEffect } from "react";
import { Col, Row, Stack } from "react-bootstrap";
import SearchQueryInput from "./QueryInput";
import FileDisplayer from "./Displayer";
import { useDispatch, useSelector } from "./Thunk";
import { dispatchSearchResult } from "./Reducer";

export default function SearchEngine() {
  const { documents, searchResult } = useSelector((state) => state);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(dispatchSearchResult(documents));
  }, []);

  return (
    <Stack style={{ marginTop: "5rem", color: "#fff" }} gap={5}>
      <Row>
       
          <h5 style={{ color: "#fff" }}>Search parameters</h5>
          <Stack>
            <span style={{ color: "#fff" }}>name</span>
            <span style={{ color: "#fff" }}>ext</span>
            <span style={{ color: "#fff" }}>type</span>
            <span style={{ color: "#fff" }}>category</span>
            <span style={{ color: "#fff" }}>date</span>
            <span style={{ color: "#fff" }}>time</span>
            <span style={{ color: "#fff" }}>size</span>
            <span style={{ color: "#fff" }}>language</span>
            <span style={{ color: "#fff" }}>keywords</span>
            <span style={{ color: "#fff" }}>content</span>
          </Stack>
       
       
          <SearchQueryInput />
      
      </Row>
      <Row>
        <FileDisplayer documents={searchResult} />
      </Row>
    </Stack>
  );
}
