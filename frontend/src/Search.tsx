import { Col, Row, Stack } from "react-bootstrap";
import SearchQueryInput from "./QueryInput";
import FileDisplayer from "./Displayer";
import { useDispatch, useSelector } from "./Thunk";
import { useEffect } from "react";
import { dispatchSearchResult } from "./Reducer";

export default function SearchEngine() {
  const { documents, searchResult } = useSelector((state) => state);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(dispatchSearchResult(documents));
  }, []);

  return (
    <Stack style={{ marginTop: "5rem" }} gap={5}>
      <Row>
        <Col xs={4}>
          <h5>Search params</h5>
          <Stack>
            <span>name</span>
            <span>ext</span>
            <span>type</span>
            <span>category</span>
            <span>date</span>
            <span>time</span>
            <span>size</span>
            <span>language</span>
            <span>keywords</span>
            <span>content</span>
          </Stack>
        </Col>
        <Col xs={8}>
          <SearchQueryInput />
        </Col>
      </Row>
      <Row>
        <FileDisplayer documents={searchResult} />
      </Row>
    </Stack>
  );
}