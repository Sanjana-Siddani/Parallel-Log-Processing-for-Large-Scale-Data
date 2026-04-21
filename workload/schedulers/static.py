from collections import Counter
from multiprocessing import Pool

def parse_line(line):
    parts = line.strip().split(" ",2)
    level = parts[0].strip("[]")
    ip = parts[1]
    message = parts[2] if len(parts) > 2 else ""
    return level, ip, message

def process_chunk(lines):
    level_counts = Counter()
    ip_counts = Counter()
    for line in lines:
        if not line.strip():
            continue

        level,ip,message = parse_line(line)
        level_counts[level] += 1
        ip_counts[ip] += 1
    return level_counts, ip_counts

def split_into_chunks(lines, num_workers):
    chunk_size = len(lines) // num_workers
    chunks = []
    start = 0

    for i in range(num_workers):
        end = start + chunk_size
        if i == num_workers - 1:
            end = len(lines)
        chunks.append(lines[start:end])
        start = end
    return chunks

def merge_results(results):
    total_level_counts = Counter()
    total_ip_counts = Counter()

    for level_counts, ip_counts in results:
        total_level_counts.update(level_counts)
        total_ip_counts.update(ip_counts)

    return total_level_counts, total_ip_counts  

def static_schedule(file_path, num_workers=4,top_n=3):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    chunks = split_into_chunks(lines, num_workers)

    with Pool(num_workers) as pool:
        results = pool.map(process_chunk, chunks)

    total_level_counts, total_ip_counts = merge_results(results)
    top_ips = total_ip_counts.most_common(top_n)

    return total_level_counts, total_ip_counts, top_ips


if __name__ == "__main__":
    log_file_path = "../../logs.txt"

    level_counts, ip_counts, top_ips = static_schedule(log_file_path, num_workers=4, top_n=3)

    print("Static Scheduling Results")
    print("\nLog Level Counts:")
    for level, count in level_counts.items():
        print(f"{level}: {count}")

    print("\nIP Address Counts:")
    for ip, count in ip_counts.items():
        print(f"{ip}: {count}")

    print("\nTop IP Addresses:")
    for ip, count in top_ips:
        print(f"{ip}: {count}")