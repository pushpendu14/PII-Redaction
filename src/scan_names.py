from docx import Document
from src.detectors import detect_names


document = Document("input/Red Herring Prospectus.docx")

total = 0

for paragraph in document.paragraphs:
    results = detect_names(paragraph.text)

    for result in results:
        print(result)
        total += 1

print()
print(f"Total names detected in paragraphs: {total}")