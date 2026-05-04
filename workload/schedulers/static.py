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


def static_schedule(file_path, num_workers=4, top_n=3):
    start = time.perf_counter()

    # open file and read lines
    f = open(file_path, 'r', encoding='latin-1')
    lines = f.readlines()
    f.close()

    # split lines into equal chunks
    chunks = split_into_chunks(lines, num_workers)

    # create pool manually
    pool = Pool(num_workers)
    results = pool.map(process_chunk, chunks)
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

    counts, top_ips, t = static_schedule(log_file_path)

    print("Static Time:", t)
    print("Top IPs:", top_ips)
