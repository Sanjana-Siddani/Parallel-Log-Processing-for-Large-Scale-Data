import random
from collections import Counter

LOG_LEVELS = ["INFO", "ERROR", "WARN"]

MESSAGES = [
    "User logged in",
    "File accessed",
    "Timeout",
    "Disk Full",
    "CPU utilization high",
    "Request processed"
]


def generate_ip_pool(n):
    ips = []
    for i in range(n):
        third = i // 256
        fourth = i % 256
        ip = f"192.168.{third}.{fourth}"
        ips.append(ip)
    return ips


def pick_random_ip(ips, num_lines):
    selected_ips = []
    for i in range(num_lines):
        ip = random.choice(ips)
        selected_ips.append(ip)
    return selected_ips


def pick_skewed_ips(ips, num_lines, s):
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


def generate_log_line(selected_ip):
    log_lines = []

    for ip in selected_ip:
        level = random.choice(LOG_LEVELS)
        message = random.choice(MESSAGES)

        line = f"[{level}] {ip} {message}"
        log_lines.append(line)
    return log_lines


def write_logs_to_file(log_lines, output_path):
    with open(output_path, 'w') as f:
        for line in log_lines:
            f.write(line + '\n')


if __name__ == "__main__":
    ips = generate_ip_pool(5)
    selected = pick_skewed_ips(ips, 10, s=1.0)

    # counts = Counter(selected)
    logs = generate_log_line(selected)

    write_logs_to_file(logs, "logs.txt")
    print("Generated logs written to logs.txt")
