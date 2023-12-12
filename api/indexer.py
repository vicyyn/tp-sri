import json
from datetime import datetime
from typing import Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from PIL import Image
import pytesseract

nltk.download('stopwords')
nltk.download('punkt')


class IndexManager:
    def __init__(self, indexPath: str):
        self.indexPath = indexPath
        self.dataIndex = self.loadIndex()

    def loadIndex(self) -> Dict:
        try:
            with open(self.indexPath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def saveIndex(self) -> None:
        with open(self.indexPath, 'w') as file:
            json.dump(self.dataIndex, file)

    def extractTextFromImage(self, imagePath: str) -> str:
        try:
            image = Image.open(imagePath)
            output = pytesseract.image_to_string(image)
            print(output)
            return output
        except Exception as e:
            print(f"Error during OCR: {str(e)}")
            return ""

    def addToIndex(self, category: str, value: str, doc) -> None:
        if value not in self.dataIndex[category]:
            self.dataIndex[category][value] = []
        self.dataIndex[category][value].append(doc.path)

    def processDocumentContent(self, doc) -> None:
        content = self.extractTextFromImage(doc.path) if "png" in doc.type else self.readDocument(doc.path)
        self.indexContent(content, doc.path)

    def readDocument(self, filePath: str) -> str:
        with open(filePath, 'r', encoding='utf-8') as file:
            return file.read()

    def indexContent(self, content: str, filePath: str) -> None:
        sentences = sent_tokenize(content)
        ignoredWords = set(stopwords.words('english'))
        contentIndex = {}

        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            relevantWords = [word for word in words if word.isalnum() and word not in ignoredWords]

            for word in relevantWords:
                contentIndex[word] = contentIndex.get(word, 0) + 1

        for word, occurrences in contentIndex.items():
            if word not in self.dataIndex['content']:
                self.dataIndex['content'][word] = []
            self.dataIndex['content'][word].append({"filePath": filePath, "occurrences": occurrences})

    def updateDocumentIndex(self, doc) -> None:
        self.addToIndex("name", doc.name, doc)
        self.addToIndex("type", doc.type, doc)
        self.addToIndex("size", doc.size, doc)
        self.addToIndex("ext", doc.ext, doc)

        if doc.language:
            self.addToIndex("language", doc.language, doc)

        if doc.category:
            self.addToIndex("category", doc.category, doc)

        if doc.keywords:
            for keyword in doc.keywords.split(','):
                self.addToIndex("keywords", keyword.strip(), doc)

        if doc.date:
            dateObj = datetime.strptime(doc.date, "%Y-%m-%d %H:%M:%S")
            self.addToIndex("date", dateObj.strftime('%Y-%m-%d'), doc)
            self.addToIndex("time", dateObj.strftime('%H:%M:%S'), doc)

        self.processDocumentContent(doc)
        self.saveIndex()


# Example usage
# indexManager = IndexManager("./indexes/index.json")
# Example document object should be provided here
# indexManager.updateDocumentIndex(document)
