import os
import mimetypes
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import re
from indexer import IndexManager
from evaluator import QueryEvaluator

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search-engine.db'
db = SQLAlchemy(app)
CORS(app)
index_manager = IndexManager("./indexes/index.json")
query_evaluator = QueryEvaluator()

# Document model
class Document(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  path = db.Column(db.String(20), unique=True, nullable=False)
  name = db.Column(db.String(120))
  ext = db.Column(db.String(120))
  date = db.Column(db.String(255))
  type = db.Column(db.String(255))
  language = db.Column(db.String(255))
  keywords = db.Column(db.String(255))
  category = db.Column(db.String(255))
  size = db.Column(db.Integer)

  @staticmethod
  def to_json(document):
    """
    Convert a document instance to JSON format.
    """
    return {
      'id': document.id,
      'path': document.path,
      'name': document.name,
      'ext': document.ext,
      'date': document.date,
      'type': document.type,
      'language': document.language,
      'keywords': document.keywords,
      'category': document.category,
      'size': document.size
    }

  @staticmethod
  def getAll():
    """
    Retrieve all documents from the database.
    """
    documents = Document.query.all()
    return [Document.to_json(doc) for doc in documents]

# Flask routes
@app.route('/documents', methods=['GET'])
def documents():
  return jsonify(Document.getAll())

@app.route('/indexes', methods=['GET'])
def indexes():
  db.create_all()
  return jsonify(index_manager.dataIndex)

@app.route('/search', methods=['POST'])
def search_docs():
  query = request.form.get('query')
  print(index_manager.dataIndex)
  transformed_query = query_evaluator.filter_index(query, index_manager.dataIndex)
  print(transformed_query)
  paths = list(set([doc['filePath'] for doc in transformed_query]))
  return jsonify([Document.to_json(document) for document in Document.query.filter(Document.path.in_(paths)).all()])

@app.route('/indexes', methods=['POST'])
def updateIndex():
  if 'document' not in request.files:
    return jsonify({}), 500

  file = request.files['document']
  if file.filename == '':
      return jsonify({}), 500

  path = './documents/' + file.filename
  file.save(path)

  # Assuming the file properties are similar to your previous example
  new_document = Document(
      path=path,
      name=os.path.splitext(file.filename)[0],
      ext=os.path.splitext(file.filename)[1].lstrip("."),
      type=mimetypes.guess_type(path)[0],
      date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      language=request.form.get('language'),
      category=request.form.get('category'),
      keywords=request.form.get('keywords'),
      size=os.path.getsize(path),
  )

  index_manager.updateDocumentIndex(new_document)
  db.session.add(new_document)
  db.session.commit()

  return jsonify({
      "indexes": index_manager.dataIndex,
      'documents': Document.getAll()
  })

# Main
if __name__ == '__main__':
    # Ensure that the database and tables are created
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=8000)

