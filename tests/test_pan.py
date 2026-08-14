from src.detectors import detect_pans


valid_text = """
PAN: ABCDE1234F
Another PAN: XYZAB9876C
"""


invalid_text = """
Invalid: ABC1234F
Invalid: ABCDE12345
Invalid: 12345ABCDE
"""


print("========== VALID PAN TESTS ==========")

for result in detect_pans(valid_text):
    print(result)


print("\n========== INVALID PAN TESTS ==========")

for result in detect_pans(invalid_text):
    print(result)