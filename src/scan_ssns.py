from docx import Document
from src.detectors import detect_ssns


document = Document("input/Red Herring Prospectus.docx")

total = 0

for paragraph in document.paragraphs:

    results = detect_ssns(paragraph.text)

    for result in results:
        print(result)
        total += 1

print(f"\nTotal SSNs detected in paragraphs: {total}")