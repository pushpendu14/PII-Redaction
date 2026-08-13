from src.detectors import detect_phones

test_text = """
Call us at +91 20 45053237.
Another number is +91 (20) 6729 5100.
You can also contact 020-45053237.
This is a financial number 1234567890.
"""

results = detect_phones(test_text)
for result in results:
    print(result)