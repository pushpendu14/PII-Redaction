from docx import Document
from src.detectors import detect_credit_cards


document = Document("input/Red Herring Prospectus.docx")


for paragraph in document.paragraphs:
    results = detect_credit_cards(paragraph.text)

    for result in results:
        print(result)