from .detectors import (
    detect_emails,
    detect_phones,
    detect_ssns,
    detect_credit_cards,
    detect_ip_addresses,
    detect_pans,
    detect_names,
)


def detect_all(text):
    results = []

    results.extend(detect_emails(text))
    results.extend(detect_phones(text))
    results.extend(detect_ssns(text))
    results.extend(detect_credit_cards(text))
    results.extend(detect_ip_addresses(text))
    results.extend(detect_pans(text))
    results.extend(detect_names(text))

    return results