from src.detectors import detect_credit_cards


test_cases = [
    "Valid test card: 4111111111111111",
    "Valid formatted card: 4111 1111 1111 1111",
    "Valid formatted card: 4111-1111-1111-1111",
    "Invalid number: 4111111111111112",
    "Ordinary number: 1234567890123456",
]


for text in test_cases:
    results = detect_credit_cards(text)

    print()
    print(text)
    print(results)