import re
import spacy

nlp = spacy.load("en_core_web_sm")

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

        context_start = max(0, match.start() - 40)
        context_end = min(len(text), match.end() + 40)

        context = text[context_start:context_end].lower()

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

        if not is_phone_context:

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

            if "-" in value:
                continue

            # Reject values that are part of an IP address
            if "." in value:
                continue

        results.append({
            "type": "PHONE",
            "text": value,
            "start": match.start(),
            "end": match.end()
        })

    return results


def detect_ssns(text):
    results = []

    for match in SSN_PATTERN.finditer(text):
        results.append({
            "type": "SSN",
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    return results


CREDIT_CARD_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\d[ -]?){13,19}"
    r"(?!\d)"
)

IP_PATTERN = re.compile(
    r'(?<![\d.])'
    r'(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)'
    r'(?!\d)'
)
PAN_PATTERN = re.compile(
    r"(?<![A-Z0-9])"
    r"[A-Z]{5}[0-9]{4}[A-Z]"
    r"(?![A-Z0-9])"
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

    return results

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

def detect_pans(text):
    results = []

    for match in PAN_PATTERN.finditer(text):
        results.append({
            "type": "PAN",
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    return results

NAME_BLACKLIST = {
    "offer",
    "offers",
    "director",
    "directors",
    "promoter",
    "promoters",
    "email",
    "website",
    "telephone",
    "mobile",
    "address",
    "registrar",
    "bid",
    "bidder",
    "bidders",
    "floor",
    "reference rate",
    "mutual funds",
    "selling shareholder",
    "share transfer agents",
    "key managerial personnel",
}


NAME_CONTEXT_BLACKLIST = {
    # Business / organization context
    "private limited",
    "limited",
    "ltd",
    "llp",
    "inc",
    "corporation",
    "company",
    "co.",
    "enterprises",
    "industries",
    "industrial park",
    "industrial",
    "group",
    "holdings",
    "trust",
    "foundation",
    "facility",
    "complex",

    # Location / address context
    "taluka",
    "marg",
    "road",
    "rd",
    "street",
    "st",
    "nagar",
    "east",
    "west",
    "north",
    "south",
    "showroom",
    "hospital",
    "bhavan",
    "building",
    "chambers",
    "opposite",
    "opp",

    # Document / financial context
    "website",
    "email",
    "registered broker",
    "bidders",
    "bid amount",
    "dp id",

    # Document phrases
    "secondary transfer",
    "transfer of",
    "listing",
    "transfer",
    "offer for",
    "issue of",
    "sale of",
    "purchase of",
    "acquisition of",
}

def contains_non_person_indicator(name):
    """
    Reject entities that contain words commonly associated
    with companies, organizations, buildings, or locations.
    """

    name_lower = name.lower()

    indicators = {
        # Business / organization
        "limited",
        "ltd",
        "llp",
        "inc",
        "corporation",
        "company",
        "enterprises",
        "industries",
        "industrial",
        "group",
        "holdings",
        "trust",
        "foundation",

        # Location / address
        "road",
        "rd",
        "street",
        "st",
        "nagar",
        "east",
        "west",
        "north",
        "south",
        "marg",
        "bhavan",
        "building",
        "opposite",
        "opp",
        "taluka",
    }

    words = name_lower.split()

    return any(word in indicators for word in words)


def is_likely_person_name(name):
    """
    Basic structural validation for a human name.
    """

    parts = name.split()

    # A person's name should normally have at least two words
    if len(parts) < 2:
        return False

    # Reject extremely long entity phrases
    if len(parts) > 5:
        return False

    # Every part should contain alphabetic characters
    for part in parts:
        if not any(char.isalpha() for char in part):
            return False

    return True


def detect_names(text):
    results = []

    doc = nlp(text)

    for ent in doc.ents:

        # Only consider entities classified by spaCy as PERSON
        if ent.label_ != "PERSON":
            continue

        name = ent.text.strip()
        name_lower = name.lower()

        # Rule 1: reject known non-person terms
        if name_lower in NAME_BLACKLIST:
            continue

        # Rule 2: reject names containing digits
        if any(char.isdigit() for char in name):
            continue

        # Rule 3: reject email-like entities
        if "@" in name:
            continue

        # Rule 4: reject known business/location phrases
        if any(
            phrase in name_lower
            for phrase in NAME_CONTEXT_BLACKLIST
        ):
            continue

        # Rule 5: reject organization/location indicators
        if contains_non_person_indicator(name):
            continue

        # Rule 6: validate human-name structure
        if not is_likely_person_name(name):
            continue

        # Rule 7: reject entities containing slash separators
        if "/" in name:
            continue

        # Valid PERSON entity
        results.append({
            "type": "PERSON",
            "text": name,
            "start": ent.start_char,
            "end": ent.end_char
        })

    return results
