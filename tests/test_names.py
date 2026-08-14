from src.detectors import detect_names


text = """
Sarthak Malvadkar is the Company Secretary.
Prakash Boricha is the Contact Person.
Kishan Rastogi and Abhijit Diwan are contact persons.
"""


results = detect_names(text)

print("========== DETECTED NAMES ==========")

for result in results:
    print(result)