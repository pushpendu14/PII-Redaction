from docx import Document
from src.detectors import detect_pans


document = Document("input/Red Herring Prospectus.docx")

total = 0

for paragraph in document.paragraphs:
    results = detect_pans(paragraph.text)

    for result in results:
        print(result)
        total += 1

print()
print(f"Total PANs detected in paragraphs: {total}")