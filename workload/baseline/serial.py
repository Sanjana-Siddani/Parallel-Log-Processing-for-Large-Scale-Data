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