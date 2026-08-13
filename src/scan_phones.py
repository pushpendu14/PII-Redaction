from docx import Document
from src.detectors import detect_phones


document = Document("input/Red Herring Prospectus.docx")

total = 0

for paragraph in document.paragraphs:

    results = detect_phones(paragraph.text)

    for result in results:
        print(result)
        total += 1


print("\nTotal phones detected in paragraphs:", total)