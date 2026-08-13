from src.detectors import detect_ssns


text = """
Valid SSN: 123-45-6789
Another valid SSN: 987 65 4321

Invalid SSN: 000-12-3456
Invalid SSN: 666-12-3456
"""


print("Detected SSNs:")

for result in detect_ssns(text):
    print(result)