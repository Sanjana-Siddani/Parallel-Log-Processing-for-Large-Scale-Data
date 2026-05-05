<<<<<<< HEAD
import time
from collections import Counter
from multiprocessing import Pool


def parse_line(line):
    parts = line.strip().split("\t")  # TAB split

    if len(parts) < 1:
        return None

    ip = parts[0]
    return ip


def process_chunk(chunk):
    ip_counts = Counter()

    for line in chunk:
        if not line.strip():
            continue

        ip = parse_line(line)
        if ip is None:
            continue

        ip_counts[ip] += 1

    return ip_counts


def make_chunks(lines, chunk_size):
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunks.append(lines[i:i + chunk_size])
    return chunks


def dynamic_schedule(file_path, num_workers=4, top_n=3, chunk_size=1000):
    start = time.perf_counter()

    # open file and read lines
    f = open(file_path, 'r', encoding='latin-1')
    lines = f.readlines()
    f.close()

    # split into smaller chunks
    chunks = make_chunks(lines, chunk_size)

    # create pool manually
    pool = Pool(num_workers)
    results = list(pool.imap_unordered(process_chunk, chunks))
    pool.close()
    pool.join()

    total_ip_counts = Counter()
    for r in results:
        total_ip_counts.update(r)

    top_ips = total_ip_counts.most_common(top_n)

    end = time.perf_counter()
    return total_ip_counts, top_ips, (end - start)


if __name__ == "__main__":
    log_file_path = "log_1.tsv"

    counts, top_ips, t = dynamic_schedule(log_file_path)

    print("Dynamic Time:", t)
    print("Top IPs:", top_ips)
=======
from collections import Counter
from multiprocessing import Pool
import os
import time


def parse_line(line):
    parts = line.strip().split(" ", 2)
    level = parts[0].strip("[]")
    ip = parts[1]
    message = parts[2] if len(parts) > 2 else ""
    return level, ip, message


def process_chunk(chunk_data):
    chunk_id, lines = chunk_data

    level_counts = Counter()
    ip_counts = Counter()

    pid = os.getpid()
    start = time.time()

    print(f"Worker {pid} started processing chunk {chunk_id} with {len(lines)} lines")

    for line in lines:
        if not line.strip():
            continue

        level, ip, message = parse_line(line)
        level_counts[level] += 1
        ip_counts[ip] += 1

    end = time.time()
    print(f"Worker {pid} finished chunk {chunk_id} in {end - start:.4f} seconds")

    return level_counts, ip_counts


def make_small_chunks(lines, chunk_size):
    chunks = []

    for i in range(0, len(lines), chunk_size):
        chunks.append((i // chunk_size, lines[i:i + chunk_size]))

    return chunks


def merge_results(results):
    total_level_counts = Counter()
    total_ip_counts = Counter()

    for level_counts, ip_counts in results:
        total_level_counts.update(level_counts)
        total_ip_counts.update(ip_counts)

    return total_level_counts, total_ip_counts


def dynamic_schedule(file_path, num_workers=4, top_n=3, chunk_size=2):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    chunks = make_small_chunks(lines, chunk_size)

    with Pool(num_workers) as pool:
        results = pool.imap_unordered(process_chunk, chunks)

        collected_results = []
        for result in results:
            collected_results.append(result)

    total_level_counts, total_ip_counts = merge_results(collected_results)
    top_ips = total_ip_counts.most_common(top_n)

    return total_level_counts, total_ip_counts, top_ips


if __name__ == "__main__":
    log_file_path = "../../logs.txt"
    level_counts, ip_counts, top_ips = dynamic_schedule(
        log_file_path,
        num_workers=4,
        top_n=3,
        chunk_size=2
    )

    print("Dynamic Schedule Results:")

    print("\nLog Level Counts:")
    for level, count in level_counts.items():
        print(f"{level}: {count}")

    print("\nIP Address Counts:")
    for ip, count in ip_counts.items():
        print(f"{ip}: {count}")

    print("\nTop IP Addresses:")
    for ip, count in top_ips:
        print(f"{ip}: {count}")
>>>>>>> 729fdc6 (Save local changes)
