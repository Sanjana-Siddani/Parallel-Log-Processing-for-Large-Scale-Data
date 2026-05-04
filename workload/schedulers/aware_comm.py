import time
from collections import Counter
from multiprocessing import Pool
from src.generator.utils import simulate_comm_cost


def parse_line(line):
    parts = line.strip().split("\t")  # TAB split is used to separate files

    if len(parts) < 1:
        return None

    ip = parts[0]
    return ip


def process_chunk(lines):
    # Count how many times the same IP appears.
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
    # Create buckets for each worker based on a hash.
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


def comm_aware_schedule(file_path, num_workers=4, top_n=3, alpha=0):
    start = time.perf_counter()

    # open file and read lines
    f = open(file_path, 'r', encoding='latin-1')
    lines = f.readlines()
    f.close()

    # build communication-aware buckets
    buckets = build_buckets(lines, num_workers)

    # create pool manually
    # pool means we are creating a pool of worker processes that can run concurrently.
    pool = Pool(num_workers)
    results = pool.map(process_chunk, buckets)
    pool.close()
    pool.join()

    # simulate communication cost
    size, comm_delay = simulate_comm_cost(results, alpha)

    total_ip_counts = Counter()
    for r in results:
        total_ip_counts.update(r)

    top_ips = total_ip_counts.most_common(top_n)

    end = time.perf_counter()
    return total_ip_counts, top_ips, (end - start), size, comm_delay


if __name__ == "__main__":
    log_file_path = "log_1.tsv"  # Logs path

    counts, top_ips, t, size, comm = comm_aware_schedule(
        log_file_path,
        num_workers=4,
        alpha=1e-6,
        top_n=3
    )

    print("Comm-aware Time:", t)
    print("Top IPs:", top_ips)
    print("Size:", size)
    print("Communication Delay:", comm)
