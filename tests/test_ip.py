from src.detectors import detect_ip_addresses


valid_ips = """
192.168.1.1
10.0.0.1
172.16.254.1
255.255.255.255
0.0.0.0
"""

invalid_ips = """
999.999.999.999
256.1.1.1
192.168.1.300
"""


print("========== VALID IP TESTS ==========")

for result in detect_ip_addresses(valid_ips):
    print(result)


print("\n========== INVALID IP TESTS ==========")

for result in detect_ip_addresses(invalid_ips):
    print(result)