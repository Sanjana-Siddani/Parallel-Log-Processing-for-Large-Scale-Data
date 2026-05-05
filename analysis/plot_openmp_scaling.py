import matplotlib.pyplot as plt

threads = [1, 2, 4, 8]

openmp_times = [0.101, 0.055, 0.029, 0.027]
thread_times = [0.099, 0.051, 0.027, 0.021]

plt.figure(figsize=(7,5))
plt.plot(threads, openmp_times, marker='o', label='OpenMP')
plt.plot(threads, thread_times, marker='o', label='std::thread')

plt.xlabel("Threads")
plt.ylabel("Execution Time (seconds)")
plt.title("OpenMP vs std::thread Performance")
plt.legend()
plt.grid(True)

plt.savefig("analysis/openmp_vs_threads.png")