from src.detectors import detect_ip_addresses


test_text = """
Valid IPs:
192.168.1.1
10.0.0.1
172.16.254.1
255.255.255.255

Invalid IPs:
999.999.999.999
256.1.1.1
192.168.1.300
"""

results = detect_ip_addresses(test_text)

for result in results:
    print(result)