import Container from "react-bootstrap/Container";

import { useRoutes } from "react-router-dom";
import Indexes from "./Indexes";
import SearchEngine from "./Search";
import { useDispatch } from "./Thunk";
import { useEffect } from "react";
import { dispatchDocuments, dispatchIndexes } from "./Reducer";
import { toast } from "react-toastify";
import { API_PATH } from "./Consts";

function App() {
  
  const dispatch = useDispatch();

  useEffect(() => {
    (async function () {
      let response = await fetch(`${API_PATH}/indexes`);
      if (response.ok) {
        const indexes = await response.json();
        dispatch(dispatchIndexes(indexes));
      } else {
        toast("An Error has occured", { type: "error", autoClose: 2000 });
      }

      response = await fetch(`${API_PATH}/documents`);
      if (response.ok) {
        const documents = await response.json();
        dispatch(dispatchDocuments(documents));
      } else {
        toast("An Error has occured", { type: "error", autoClose: 2000 });
      }
    })();
  }, []);

  return (
    <>
      

      <Container>
        <Indexes>
        </Indexes>
        <SearchEngine>

        </SearchEngine>
        </Container>
    </>
  );
}

export default App;