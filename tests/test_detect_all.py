from src.detect_all import detect_all


text = """
Contact Sarthak Malvadkar at sarthak@example.com
or call +91 81081 14949.

Server IP: 192.168.1.1

PAN: ABCDE1234F

SSN: 123-45-6789

Card: 4111111111111111
"""


results = detect_all(text)

print("========== ALL DETECTED PII ==========")

for result in results:
    print(result)

print()
print("Total PII detected:", len(results))