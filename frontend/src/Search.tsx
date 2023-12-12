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
       
          <h5 style={{ color: "#fff" }}>Search parameters : name,ext,type,category,date,time,size;language,keywords,contents</h5>
          
       
       
          <SearchQueryInput />
      
      </Row>
      <Row>
        <FileDisplayer documents={searchResult} />
      </Row>
    </Stack>
  );
}
