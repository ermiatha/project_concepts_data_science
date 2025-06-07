import random
import time
import matplotlib.pyplot as plt
from ternary_search_tree import TernarySearchTree  # Make sure your class is imported from a separate file

# Load words
with open('data/search_trees/corncob_lowercase.txt') as file:
    words = [line.strip() for line in file]

# Shuffle once for randomness
random.shuffle(words)

# Benchmark parameters
sizes = [100, 500, 1_000, 5_000, 10_000, 20_000, 30_000, 40_000, 50_000]
nr_runs = 10

# === Insertion Benchmark ===
insert_sample = random.sample(words, k=20)
insert_times = {}

for size in sizes:
    sample = random.sample(words, k=size)
    tst = TernarySearchTree()
    for word in sample:
        tst.insert(word)
    insert_times[size] = 0.0
    for _ in range(nr_runs):
        start_time = time.time_ns()
        for word in insert_sample:
            tst.insert(word)
        end_time = time.time_ns()
        insert_times[size] += end_time - start_time
    insert_times[size] /= nr_runs * 1_000_000.0  # Convert to milliseconds

for sample in samples:
    size = len(sample)
    tst = TernarySearchTree()
    # Build tree from the sample
    for word in sample:
        tst.insert(word)
    insert_times[size] = 0.0
    for _ in range(nr_runs):
        start_time = time.time_ns()
        for word in insert_sample:
            tst.insert(word)
        end_time = time.time_ns()
        insert_times[size] += end_time - start_time
    # Average time in milliseconds
    insert_times[size] /= nr_runs * 1_000_000.0

# === Plot Insertion ===
plt.figure()
plt.plot(insert_times.keys(), insert_times.values(), marker='o')
plt.title("TST Insert Performance")
plt.xlabel("Number of words in TST")
plt.ylabel("Insert time for 20 words (ms)")
plt.grid(True)
plt.savefig("insert_tst.png")


# === Search Benchmark ===
search_sample = random.sample(words, k=20)
search_times = {}

for size in sizes:
    sample = random.sample(words, k=size)
    tst = TernarySearchTree()
    for word in sample:
        tst.insert(word)
    search_times[size] = 0.0
    for _ in range(nr_runs):
        start_time = time.time_ns()
        for word in search_sample:
            tst.search(word)
        end_time = time.time_ns()
        search_times[size] += end_time - start_time
    search_times[size] /= nr_runs * 1_000_000.0

# === Plot Search ===
plt.figure()
plt.plot(search_times.keys(), search_times.values(), marker='o', color='green')
plt.title("TST Search Performance")
plt.xlabel("Number of words in TST")
plt.ylabel("Search time for 20 words (ms)")
plt.grid(True)
plt.savefig("search_tst.png")


# === Comparison with Python set ===
hold_out_sample = words[-100:]
insert_sample = words[:-100]

# Insert: Python set
start = time.time_ns()
word_set = set()
for word in insert_sample:
    word_set.add(word)
end = time.time_ns()
set_insert_time = (end - start) / 1_000_000.0

# Insert: TST
start = time.time_ns()
word_tst = TernarySearchTree()
for word in insert_sample:
    word_tst.insert(word)
end = time.time_ns()
tst_insert_time = (end - start) / 1_000_000.0

# Search: Python set
start = time.time_ns()
_ = sum(1 for word in hold_out_sample if word in word_set)
end = time.time_ns()
set_search_time = (end - start) / 1_000_000.0

# Search: TST
start = time.time_ns()
_ = sum(1 for word in hold_out_sample if word_tst.search(word))
end = time.time_ns()
tst_search_time = (end - start) / 1_000_000.0

# === Print Comparison ===
print("Comparison with Python set:")
print(f"Set insert time: {set_insert_time:.2f} ms")
print(f"TST insert time: {tst_insert_time:.2f} ms")
print(f"Set search time: {set_search_time:.2f} ms")
print(f"TST search time: {tst_search_time:.2f} ms")