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
