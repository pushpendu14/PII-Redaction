import re

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)


def detect_emails(text):
    results = []

    for match in EMAIL_PATTERN.finditer(text):
        results.append({
            "type": "EMAIL",
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    return results

PHONE_PATTERN = re.compile(
    r"""
    (?<!\d)
    (?:
        \+?\s*91[\s.-]?
    )?
    (?:
        \(\d{2,5}\)[\s.-]?
    )?
    \d{3,5}
    (?:[\s.-]\d{3,5})+
    (?!\d)
    """,
    re.VERBOSE
)

SSN_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?!000|666|9\d{2})"
    r"\d{3}"
    r"[- ]"
    r"(?!00)"
    r"\d{2}"
    r"[- ]"
    r"(?!0000)"
    r"\d{4}"
    r"(?!\d)"
)


def detect_phones(text):
    results = []

    for match in PHONE_PATTERN.finditer(text):

        value = match.group().strip()

        # Get some surrounding text for context validation
        context_start = max(0, match.start() - 40)
        context_end = min(len(text), match.end() + 40)

        context = text[context_start:context_end].lower()

        # Words that strongly suggest that the number is a phone number
        phone_contexts = [
            "telephone",
            "phone",
            "mobile",
            "contact number",
            "contact no",
            "tel:",
            "tel."
        ]

        is_phone_context = any(
            keyword in context
            for keyword in phone_contexts
        )

        # Reject candidates that don't have strong phone context
        if not is_phone_context:

            # Reject obvious address/postal-code context
            if any(keyword in context for keyword in [
                "pune",
                "mumbai",
                "maharashtra",
                "india",
                "address",
                "office",
                "road",
                "marg",
                "nagar"
            ]):
                continue

            # Reject year ranges such as 2022-2023
            if "-" in value:
                continue

        results.append({
            "type": "PHONE",
            "text": value,
            "start": match.start(),
            "end": match.end()
        })

def detect_ssns(text):
    results = []

    for match in SSN_PATTERN.finditer(text):
        results.append({
            "type": "SSN",
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })

CREDIT_CARD_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\d[ -]?){13,19}"
    r"(?!\d)"
)

IP_PATTERN = re.compile(
    r"(?<![\d.])"
    r"(?:"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\."
    r"){3}"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"(?![\d.])"
)


def normalize_digits(value):
    return re.sub(r"\D", "", value)

def passes_luhn(number):
    digits = [int(d) for d in number]

    checksum = 0
    parity = len(digits) % 2

    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2

            if digit > 9:
                digit -= 9

        checksum += digit

    return checksum % 10 == 0


def detect_credit_cards(text):
    results = []

    for match in CREDIT_CARD_PATTERN.finditer(text):
        value = match.group().strip()

        digits = normalize_digits(value)

        if not 13 <= len(digits) <= 19:
            continue

        if not passes_luhn(digits):
            continue

        results.append({
            "type": "CREDIT_CARD",
            "text": value,
            "start": match.start(),
            "end": match.end()
        })

def detect_ip_addresses(text):
    results = []

    for match in IP_PATTERN.finditer(text):
        results.append({
            "type": "IP_ADDRESS",
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    return results