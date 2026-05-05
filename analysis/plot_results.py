import matplotlib.pyplot as plt

# Results collected from experiments
methods = ["Python Static", "Python Dynamic", "Comm-aware", "OpenMP Static"]

times = [2.80, 3.54, 3.62, 0.057]
comm_sizes = [70959, 5876376, 18262, 0]

# -------------------------------
# Graph 1: Execution Time Comparison
# -------------------------------
plt.figure(figsize=(8, 5))
plt.bar(methods, times)
plt.xlabel("Method")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time Comparison")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("analysis/execution_time_comparison.png")
plt.show()


# -------------------------------
# Graph 2: Communication Size Comparison
# -------------------------------
plt.figure(figsize=(8, 5))
plt.bar(methods, comm_sizes)
plt.xlabel("Method")
plt.ylabel("Communication Size (bytes)")
plt.title("Communication Size Comparison")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("analysis/communication_size_comparison.png")
plt.show()


# -------------------------------
# Graph 3: Time vs Communication Size
# -------------------------------
plt.figure(figsize=(7, 5))
plt.scatter(comm_sizes, times)

for i, method in enumerate(methods):
    plt.text(comm_sizes[i], times[i], method)

plt.xlabel("Communication Size (bytes)")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time vs Communication Size")
plt.tight_layout()
plt.savefig("analysis/time_vs_communication.png")
plt.show()


# -------------------------------
# Graph 4: Python-only comparison
# -------------------------------
python_methods = ["Static", "Dynamic", "Comm-aware"]
python_times = [2.80, 3.54, 3.62]
python_comm = [70959, 5876376, 18262]

plt.figure(figsize=(7, 5))
plt.bar(python_methods, python_times)
plt.xlabel("Python Scheduler")
plt.ylabel("Execution Time (seconds)")
plt.title("Python Scheduler Time Comparison")
plt.tight_layout()
plt.savefig("analysis/python_scheduler_time.png")
plt.show()


plt.figure(figsize=(7, 5))
plt.bar(python_methods, python_comm)
plt.xlabel("Python Scheduler")
plt.ylabel("Communication Size (bytes)")
plt.title("Python Scheduler Communication Comparison")
plt.tight_layout()
plt.savefig("analysis/python_scheduler_communication.png")
plt.show()