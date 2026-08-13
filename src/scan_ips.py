import sys

from detectors import detect_ip_addresses


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/scan_ips.py <file>")
        return

    file_path = sys.argv[1]

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    matches = detect_ip_addresses(text)

    print(f"Found {len(matches)} IP address(es):")

    for match in matches:
        print(match)


if __name__ == "__main__":
    main()