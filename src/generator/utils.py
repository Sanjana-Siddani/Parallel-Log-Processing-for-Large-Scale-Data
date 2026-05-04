import pickle
import time


def simulate_comm_cost(results, alpha):
    """
    Simulate communication cost by sleeping for a duration based on the result size and alpha.
    """
    size = 0

    for r in results:
        data = pickle.dumps(r)  # convert to bytes
        size += len(data)

    delay = alpha * size
    time.sleep(delay)

    return size, delay


if __name__ == "__main__":
    results = [{"a": 1}, {"b": 2}, {"c": 3}]
    # Adjust alpha as needed.
    size, delay = simulate_comm_cost(results, alpha=0.00001)
    # alpha is a scaling factor to control the delay based on size.

    print("size:", size)
    print("delay:", delay)
