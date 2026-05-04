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

    with open(file_path, 'r', encoding='latin-1') as f:
        lines = f.readlines()

    chunks = make_chunks(lines, chunk_size)

    with Pool(num_workers) as pool:
        results = list(pool.imap_unordered(process_chunk, chunks))

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
