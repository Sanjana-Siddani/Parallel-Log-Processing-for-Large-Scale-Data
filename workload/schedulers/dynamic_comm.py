import time
from collections import Counter
from multiprocessing import Pool
from src.generator.utils import simulate_comm_cost


def parse_line(line):
    parts = line.strip().split(" ", 2)

    if len(parts) < 2:
        return None

    ip = parts[1]
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


def dynamic_schedule(file_path, num_workers=4, top_n=3, chunk_size=1000, alpha=0):
    start = time.perf_counter()

    # open file and read lines
    f = open(file_path, 'r', encoding='latin-1')
    lines = f.readlines()
    f.close()

    # create smaller chunks for dynamic scheduling
    chunks = make_chunks(lines, chunk_size)

    # create pool manually
    pool = Pool(num_workers)
    results = list(pool.imap_unordered(process_chunk, chunks))
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
    log_file_path = "logs_1000000.txt"  # Logs path
    counts, top_ips, t, size, comm = dynamic_schedule(
        log_file_path,
        num_workers=4,
        chunk_size=1000,
        alpha=0,
        top_n=3
    )

    print("Time:", t)
    print("Top IPs:", top_ips)
    print("Size:", size)
    print("Communication Delay:", comm)
