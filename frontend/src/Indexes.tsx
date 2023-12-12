import {
  Accordion,
  Button,
  Container,
  Form,
  Modal,
  Row,
  Stack,
} from "react-bootstrap";
import { useDispatch, useSelector } from "./Thunk";
import { FormEvent, useState } from "react";
import { API_PATH } from "./Consts";
import { toast } from "react-toastify";
import { dispatchDocuments, dispatchIndexes } from "./Reducer";
import FileList from "./Displayer";

export default function Indexes() {
  const { indexes, documents } = useSelector((state) => state);
  const [show, setShow] = useState(false);
  const dispatch = useDispatch();

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    if (!event.target.document.files.length) {
      return;
    }

    const response = await fetch(`${API_PATH}/indexes`, {
      method: "POST",
      body: new FormData(event.target as HTMLFormElement),
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(dispatchIndexes(data.indexes));
      dispatch(dispatchDocuments(data.documents));
      setShow(false);
      toast("Indexes are updated", {
        type: "success",
        autoClose: 2000,
      });
    } else {
      toast("An error has occured", {
        type: "error",
        autoClose: 2000,
      });
    }
  };

  return (
    <>
        <Stack  >
      <Container
        style={{
          display: 'flex',
        
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          marginRight: '10px', // Add margin for spacing
        }}
      >
        <h4>Documents</h4>
        <Button onClick={() => setShow(true)} style={{
          width: "100%"
        }}>Add a document</Button>
      </Container>
      <FileList documents={documents} />

      <Container
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
        }}
      >
        <h4>Indexes</h4>
      </Container>
      <div>
      <div>
  {JSON.stringify(indexes, null, 2)}
 </div>
      </div>
    </Stack>
    <Modal show={show} onHide={() => setShow(false)} >
        <Modal.Header closeButton style={{
                background:"#444",
                color: "#fff"
              }}>
          <Modal.Title>Add a document</Modal.Title>
        </Modal.Header>
        <Modal.Body style={{
                background:"#444",
                color: "#fff"
              }}>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Document</Form.Label>
              <Form.Control type="file" name="document" />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Category</Form.Label>
              <Form.Control type="text" name="category" />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Language</Form.Label>
              <Form.Control type="text" name="language" />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Keywords (separated by ",")</Form.Label>
              <Form.Control as="textarea" rows={2} name="keywords" />
            </Form.Group>
            <Container
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "end",
              }}
            >
              <Button variant="primary" type="submit" style={{
                width: "100%"
              }}>
                Submit
              </Button>
            </Container>
          </Form>
        </Modal.Body>
      </Modal>
     
    </>
  );
}