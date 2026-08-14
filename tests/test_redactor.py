from src.detect_all import detect_all
from src.redactor import redact_text


text = """
My name is Sarthak Malvadkar.
My email is sarthak@example.com.
My phone number is +91 81081 14949.
My IP address is 192.168.1.1.
My PAN is ABCDE1234F.
My SSN is 123-45-6789.
My credit card is 4111111111111111.
"""


detections = detect_all(text)

print("========== DETECTED PII ==========")

for item in detections:
    print(item)


redacted = redact_text(text, detections)

print("\n========== REDACTED TEXT ==========")
print(redacted)