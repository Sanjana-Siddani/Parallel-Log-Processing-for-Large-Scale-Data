import random
from collections import Counter

# Log levels
LOG_LEVELS = ["INFO", "ERROR", "WARN"]

# Sample log messages
MESSAGES = [
    "User logged in",
    "File accessed",
    "Timeout",
    "Disk Full",
    "CPU utilization high",
    "Request processed"
]


def generate_ip_pool(n):
    """
    Generate n unique IP addresses in the format 192.168.x.y
    """
    ips = []
    for i in range(n):
        third = i // 256
        fourth = i % 256
        ip = f"192.168.{third}.{fourth}"
        ips.append(ip)
    return ips


def pick_random_ip(ips, num_lines):
    """
    Select IP's randomely
    """
    selected_ips = []
    for i in range(num_lines):
        ip = random.choice(ips)
        selected_ips.append(ip)
    return selected_ips


def pick_skewed_ips(ips, num_lines, s):
    """
    Select IP's with a skewed distribution based on Zipf's law with parameter s.
    """
    weights = []
    for i in range(len(ips)):
        rank = i + 1
        weight = 1 / (rank ** s)
        weights.append(weight)
    total = sum(weights)

    probabilities = []
    for w in weights:
        probabilities.append(w/total)
    selected_ips = random.choices(ips, weights=probabilities, k=num_lines)
    return selected_ips


def generate_log_lines(selected_ips):
    """
    Generate log lines for the selected IP addresses.
    """

    log_lines = []

    for ip in selected_ips:
        level = random.choice(LOG_LEVELS)
        message = random.choice(MESSAGES)

        line = f"[{level}] {ip} {message}"
        log_lines.append(line)
    return log_lines


def write_logs_to_file(log_lines, output_path):
    """
    Write the generated log lines to a file.
    """
    with open(output_path, 'w') as f:
        for line in log_lines:
            f.write(line + '\n')


if __name__ == "__main__":
    """
    Generate synthetic log data with skewed IP distribution and write to logs.txt
    """
    ips = generate_ip_pool(1000)  # Generate 1000 unique IP addresses
    sizes = [100000, 500000, 1000000]

    for size in sizes:

        print(f"Generating {size} lines...")

        selected = pick_skewed_ips(ips, size, s=1.0)

        logs = generate_log_lines(selected)

        filename = f"logs_{size}.txt"

        write_logs_to_file(logs, filename)

        print(f"{filename} created")
