import os
import PyPDF2
from PIL import Image
import pytesseract
import sqlite3
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import shutil

def classify_and_store(file_path, classification):
    base_path = "classified_documents"
    for criterion, value in classification.items():
        destination = os.path.join(base_path, criterion, value)
        os.makedirs(destination, exist_ok=True)
        shutil.copy(file_path, destination)

nltk.download('stopwords')
nltk.download('punkt')

def view_database():
    conn = sqlite3.connect('documents.db')
    c = conn.cursor()
    c.execute("SELECT * FROM documents")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()

def close_application():
    print("Closing the application.")
    exit()

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_xlsx(xlsx_path):
    workbook = openpyxl.load_workbook(xlsx_path)
    text = ""
    for sheet in workbook.sheetnames:
        worksheet = workbook[sheet]
        for row in worksheet.iter_rows(values_only=True):
            text += " ".join([str(cell) for cell in row if cell is not None]) + "\n"
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    most_common_words = Counter(filtered_words).most_common(5)
    return [word for word, count in most_common_words]

# OCR Function for Scanned Documents
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Text Extraction from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        return text

# Metadata Extraction
def extract_metadata(file_path):
    file_stats = os.stat(file_path)
    creation_time = datetime.fromtimestamp(file_stats.st_ctime)
    modification_time = datetime.fromtimestamp(file_stats.st_mtime)
    file_size = file_stats.st_size
    return creation_time, modification_time, file_size

# Indexing and Storing in Database
def index_and_store(file_path, text, metadata, keywords, manual_tags):
    conn = sqlite3.connect('documents.db')
    c = conn.cursor()

    # Update table creation to include keywords and manual_tags
    c.execute('''CREATE TABLE IF NOT EXISTS documents
                 (path TEXT, creation_time TEXT, modification_time TEXT, size INT, keywords TEXT, manual_tags TEXT)''')

    # Convert lists to strings for storage
    keywords_str = ', '.join(keywords)
    manual_tags_str = ', '.join(manual_tags)

    # Insert data including keywords and manual tags
    c.execute("INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?)", 
              (file_path, metadata[0], metadata[1], metadata[2], keywords_str, manual_tags_str))

    conn.commit()
    conn.close()

# Main Function to Process Documents
def process_document(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(('.png', '.jpg', '.jpeg')):
        text = extract_text_from_image(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.xlsx'):
        text = extract_text_from_xlsx(file_path)
    elif file_path.endswith('.txt'):
        text = extract_text_from_txt(file_path)
    else:
        text = 'Unsupported format'

    # Extract keywords
    keywords = extract_keywords(text)
    # Manual indexing
    manual_tags = input("Enter manual tags for this document, separated by commas: ").split(',')
    metadata = extract_metadata(file_path)
    index_and_store(file_path, text, metadata, keywords, manual_tags)

    classification = {
        'year': str(metadata[0].year),
        'keyword': keywords[0]  # assuming you want to classify by the most common keyword
    }
    classify_and_store(file_path, classification)

    print(f"Document indexed: {file_path}")

# Wait for User Input
if __name__ == "__main__":
    while True:
        print("\nCommands:")
        print("  index - Index a new document")
        print("  view - View indexed documents")
        print("  close - Close the application")
        command = input("Enter a command: ")

        if command.lower() == 'index':
            file_path = input("Enter the path of the file to process: ")
            process_document(file_path)
        elif command.lower() == 'view':
            view_database()
        elif command.lower() == 'close':
            close_application()
        else:
            print("Invalid command. Please try again.")