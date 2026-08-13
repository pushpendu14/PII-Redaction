from docx import Document
from src.detectors import detect_emails

document = Document("input/Red Herring Prospectus.docx")

total = 0
for paragraph in document.paragraphs:
    results = detect_emails(paragraph.text)
    for result in results:
        print(result)
        total += 1
print()
print("Total emails detected in paragraphs:", total)