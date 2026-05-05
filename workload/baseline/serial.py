<<<<<<< HEAD
from collections import Counter
import time


def parse_line(line):
    # Break down a line from the log file and extract the IP address.
    parts = line.strip().split("\t")

    if len(parts) < 1:  # if no IP found
        return None

    return parts[0]  # IP


def process_log_file(file_path, top_n):
    ip_counts = Counter()

    # open file and process line by line
    f = open(file_path, 'r', encoding='latin-1')

    for line in f:
        if not line.strip():
            continue

        ip = parse_line(line)

        if ip is None:
            continue

        ip_counts[ip] += 1

    f.close()

    top_ips = ip_counts.most_common(top_n)
    return ip_counts, top_ips


if __name__ == "__main__":
    # It processes the log file and prints the top IPs and execution time.
    log_file_path = "log_1.tsv"

    start = time.perf_counter()
    ip_counts, top_ips = process_log_file(log_file_path, top_n=3)
    end = time.perf_counter()

    print("Top IPs:")
    for ip, count in top_ips:
        print(ip, count)

    print("Time:", end - start)
=======
from collections import Counter

def parse_line(line):
    parts = line.strip().split(" ", 2)

    level = parts[0].strip("[]")
    ip = parts[1]
    message = parts[2] if len(parts) > 2 else ""
    return level, ip, message

def process_log_file(file_path, top_n):
    level_counts = Counter()
    ip_counts = Counter()

    with open(file_path, 'r') as f:
        for line in f:
            
            if not line.strip():
                continue
            level, ip, message = parse_line(line)

            level_counts[level] += 1
            ip_counts[ip] += 1

    top_ips = ip_counts.most_common(top_n)
    return level_counts, ip_counts, top_ips

if __name__ == "__main__":
    log_file_path = "../../logs.txt"

    level_counts,ip_counts, top_ips = process_log_file(log_file_path, top_n=3)

    print("Log Level Counts:")
    for level, count in level_counts.items():
        print(f"{level}: {count}")

    print("\nIP Address Counts:")
    for ip, count in ip_counts.items():
        print(f"{ip}: {count}")

    print("\nTop IP Addresses:")
    for ip, count in top_ips:
        print(f"{ip}: {count}")
>>>>>>> 729fdc6 (Save local changes)
