import time
from collections import Counter
from multiprocessing import Pool
from src.generator.utils import simulate_comm_cost


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


def split_into_chunks(lines, num_workers):
    # Divide the list of lines into equal chunks for each worker.
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


def static_schedule(file_path, num_workers=4, top_n=3, alpha=0):
    start = time.perf_counter()  # Start timer

    # open file and read lines
    f = open(file_path, 'r', encoding='latin-1')
    lines = f.readlines()
    f.close()

    # split the log lines into chunks
    chunks = split_into_chunks(lines, num_workers)

    # create pool of workers
    pool = Pool(num_workers)
    results = pool.map(process_chunk, chunks)
    pool.close()
    pool.join()

    # simulate communication cost
    size, comm_delay = simulate_comm_cost(results, alpha)

    total_ip_counts = Counter()
    for r in results:
        total_ip_counts.update(r)

    top_ips = total_ip_counts.most_common(top_n)

    end = time.perf_counter()  # End timer
    return total_ip_counts, top_ips, (end - start), size, comm_delay


if __name__ == "__main__":
    log_file_path = "log_1.tsv"

    """It processes the log file using static scheduling and prints the top IPs, execution time, size, and communication delay."""
    counts, top_ips, t, size, comm = static_schedule(
        log_file_path,
        num_workers=4,
        alpha=0,
        top_n=3
    )

    print("Static Time:", t)
    print("Top IPs:", top_ips)
    print("Size:", size)
    print("Communication Delay:", comm)
