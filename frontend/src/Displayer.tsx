import React from "react";
import { Table } from "react-bootstrap";
import type { Document } from "./Reducer";

const FileDisplayer = ({ documents }: { documents: Document[] }) => {
  function formatFileSize(sizeInBytes: number) {
    const units = ["B", "KB", "MB", "GB", "TB"];

    let size = sizeInBytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }

    size = parseFloat(size.toFixed(2));

    return size + " " + units[unitIndex];
  }

  return (
    <>
      <Table striped bordered hover style={{ background: "#333", color: "#fff" }}>
        <thead>
          <tr>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Name</th>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Ext</th>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Type</th>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Category</th>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Date Time</th>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Size</th>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Language</th>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Keywords</th>
            <th style={{ background: "#444", color: "#fff", padding: "8px" }}>Path</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((doc: Document) => (
            <tr key={doc.id}>
              <td>{doc.name ?? "-"}</td>
              <td>{doc.ext ?? "-"}</td>
              <td>{doc.type ?? "-"}</td>
              <td>{doc.category ?? "-"}</td>
              <td>{doc.date ?? "-"}</td>
              <td>{doc.size ? formatFileSize(doc.size) : "-"}</td>
              <td>{doc.language ?? "-"}</td>
              <td>{doc.keywords ?? "-"}</td>
              <td>{doc.path ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </Table>
      {documents.length === 0 && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginTop: "-1rem",
            border: "0.5px solid #dee2e6",
            borderTop: "0px solid white",
            background: "#333",
            color: "#fff",
          }}
        >
          No Documents
        </div>
      )}
    </>
  );
};

export default FileDisplayer;
