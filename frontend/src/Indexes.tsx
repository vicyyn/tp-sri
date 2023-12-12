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
        <Stack gap={3} style={{ marginTop: '3rem', marginBottom: '3rem', display: 'flex' }}>
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
        <Button onClick={() => setShow(true)}>Add a document</Button>
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
     
    </>
  );
}