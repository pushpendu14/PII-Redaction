from docx import Document
from src.detectors import detect_phones


document = Document("input/Red Herring Prospectus.docx")

for paragraph_number, paragraph in enumerate(document.paragraphs):

    results = detect_phones(paragraph.text)

    for result in results:

        start = result["start"]
        end = result["end"]

        # Show some text around the detected number
        context_start = max(0, start - 50)
        context_end = min(len(paragraph.text), end + 50)

        context = paragraph.text[context_start:context_end]

        print("=" * 80)
        print("Paragraph:", paragraph_number)
        print("Detected:", result["text"])
        print("Context:", context)