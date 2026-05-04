import time
from collections import Counter
from multiprocessing import Pool


def parse_line(line):
    parts = line.strip().split("\t")  # TAB split

    if len(parts) < 1:
        return None

    ip = parts[0]
    return ip


def process_chunk(lines):
    ip_counts = Counter()

    for line in lines:
        if not line.strip():
            continue

        ip = parse_line(line)
        if ip is None:
            continue

        ip_counts[ip] += 1

    return ip_counts


def build_buckets(lines, num_workers):
    buckets = [[] for _ in range(num_workers)]

    for line in lines:
        if not line.strip():
            continue

        ip = parse_line(line)
        if ip is None:
            continue

        worker_id = hash(ip) % num_workers
        buckets[worker_id].append(line)

    return buckets


def comm_aware_schedule(file_path, num_workers=4, top_n=3):
    start = time.perf_counter()

    # open file and read lines
    f = open(file_path, 'r', encoding='latin-1')
    lines = f.readlines()
    f.close()

    # create buckets based on communication-aware logic
    buckets = build_buckets(lines, num_workers)

    # create pool manually
    pool = Pool(num_workers)
    results = pool.map(process_chunk, buckets)
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

    counts, top_ips, t = comm_aware_schedule(log_file_path)

    print("Comm-aware Time:", t)
    print("Top IPs:", top_ips)
