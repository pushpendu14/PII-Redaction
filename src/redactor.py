def redact_text(text, detections):
    """
    Replace detected PII with [TYPE] placeholders.
    """

    # Important:
    # Replace from right to left so that character
    # positions do not change while we are editing.
    detections = sorted(
        detections,
        key=lambda x: x["start"],
        reverse=True
    )

    redacted_text = text

    for item in detections:
        start = item["start"]
        end = item["end"]
        pii_type = item["type"]

        replacement = f"[{pii_type}]"

        redacted_text = (
            redacted_text[:start]
            + replacement
            + redacted_text[end:]
        )

    return redacted_text