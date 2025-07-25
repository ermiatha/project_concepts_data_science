"""
benchmark_tst.py

This script benchmarks the performance of a Ternary Search Tree (TST) in terms of insert and search time, across increasing tree sizes. It also compares TST performance to Python's built-in set().
"""
import random
import time
import matplotlib.pyplot as plt
from ternary_search_tree import TernarySearchTree  # Import your custom TST class

# -------------------------------
# LOAD DATASET
# -------------------------------
# Load English words from file and strip whitespace
with open('data/search_trees/corncob_lowercase.txt') as file:
    words = [line.strip() for line in file]

# Check length of words loaded
len(words)

# The words are alphabetically ordered
words[:20]

# Shuffle to ensure random distribution (avoids insertion bias)
# random.shuffle(words)

# -------------------------------
# BENCHMARK PARAMETERS
# -------------------------------
sizes = [100, 500, 1_000, 5_000, 10_000, 20_000, 30_000, 40_000, 50_000]  # Sizes of trees to build
nr_runs = 300  # Number of benchmark runs to average timing results

# create a list of random samples for each size
samples = [
    random.sample(words, k=size) for size in sizes
]

# -------------------------------
# INSERTION BENCHMARK
# -------------------------------
# We can now time how long it takes to insert words into a Ternary Search Tree of various sizes.  First we build the TST based on the sample, and then we insert words.
insert_sample = random.sample(words, k=20)  # Fixed 20-word sample to test insert time
insert_times = {}

# Benchmark insert performance as tree size increases
for sample in samples:
    tst = TernarySearchTree()

    # First, build the tree with the sample size
    for word in sample:
        tst.insert(word)

    insert_times[len(sample)] = 0.0

    # Measure the time to insert 20 new words (multiple runs for averaging)
    for _ in range(nr_runs):
        start_time = time.time_ns()
        for word in insert_sample:
            tst.insert(word)
        end_time = time.time_ns()
        insert_times[len(sample)] += end_time - start_time

    # Average over number of runs and convert to milliseconds
    insert_times[len(sample)] /= nr_runs * 1_000_000.0
insert_times

# -------------------------------
# PLOT INSERTION RESULTS
# -------------------------------
plt.figure()
plt.plot(insert_times.keys(), insert_times.values(), marker='o')
plt.title("TST Insert Performance")
plt.xlabel("Number of words in TST")
plt.ylabel("Insert time for 20 words (ms)")
plt.grid(True)
plt.savefig("results/insert_tst.png")

# -------------------------------
# SEARCH BENCHMARK
# -------------------------------
search_sample = random.sample(words, k=20)  # Fixed 20-word sample to test search time
search_times = {}

# Measure search performance for increasing tree size
for size in sizes:
    sample = random.sample(words, k=size)
    tst = TernarySearchTree()

    for word in sample:
        tst.insert(word)

    search_times[size] = 0.0

    # Measure the time to search 20 words (average over multiple runs)
    for _ in range(nr_runs):
        start_time = time.time_ns()
        for word in search_sample:
            tst.search(word)
        end_time = time.time_ns()
        search_times[size] += end_time - start_time

    # Average and convert to milliseconds
    search_times[size] /= nr_runs * 1_000_000.0

# -------------------------------
# PLOT SEARCH RESULTS
# -------------------------------
plt.figure()
plt.plot(search_times.keys(), search_times.values(), marker='o', color='green')
plt.title("TST Search Performance")
plt.xlabel("Number of words in TST")
plt.ylabel("Search time for 20 words (ms)")
plt.grid(True)
plt.savefig("results/search_tst.png")

# -------------------------------
# COMPARISON: TST vs Python Set
# -------------------------------
# Separate hold-out sample
hold_out_sample = words[-100:]
insert_sample = words[:-100]

# Time Python set insertion
start = time.time_ns()
word_set = set()
for word in insert_sample:
    word_set.add(word)
end = time.time_ns()
set_insert_time = (end - start) / 1_000_000.0  # ms

# Time TST insertion
start = time.time_ns()
word_tst = TernarySearchTree()
for word in insert_sample:
    word_tst.insert(word)
end = time.time_ns()
tst_insert_time = (end - start) / 1_000_000.0

# Time Python set search
start = time.time_ns()
for word in hold_out_sample:
    _ = word in word_set
end = time.time_ns()
set_search_time = (end - start) / 1_000_000.0

# Time TST search
start = time.time_ns()
for word in hold_out_sample:
    word_tst.search(word, exact=True)
end = time.time_ns()
tst_search_time = (end - start) / 1_000_000.0

# Plot comparison bar chart
plt.figure()
plt.bar(['Set Insert', 'TST Insert'], [set_insert_time, tst_insert_time], color=['blue', 'orange'])
plt.title("Insert Time: Python Set vs TST")
plt.ylabel("Time (ms)")
plt.savefig("results/insert_comparison.png")

plt.figure()
plt.bar(['Set Search', 'TST Search'], [set_search_time, tst_search_time], color=['blue', 'orange'])
plt.title("Search Time: Python Set vs TST")
plt.ylabel("Time (ms)")
plt.savefig("results/search_comparison.png")

# -------------------------------
# BEST & WORST CASE INSERTION AND SEARCH (with averaging)
# -------------------------------

best_insert_times = {}
worst_insert_times = {}
best_search_times = {}
worst_search_times = {}

def median_first_order(words):
    if not words:
        return []
    mid = len(words) // 2
    return [words[mid]] + median_first_order(words[:mid]) + median_first_order(words[mid+1:])

for size in sizes:
    # ------------------------------------------
    # BEST CASE: Balanced (median-first insertion)
    # ------------------------------------------
    sorted_sample = sorted(random.sample(words, k=size))
    best_ordered_sample = median_first_order(sorted_sample)

    # Insert benchmark
    best_insert_times[size] = 0.0
    for _ in range(nr_runs):
        tst = TernarySearchTree()
        start = time.time_ns()
        for word in best_ordered_sample:
            tst.insert(word)
        end = time.time_ns()
        best_insert_times[size] += (end - start)
    best_insert_times[size] /= nr_runs * 1_000_000.0

    # Search benchmark (same 20 words from tree)
    best_search_times[size] = 0.0
    for _ in range(nr_runs):
        tst = TernarySearchTree()
        for word in best_ordered_sample:
            tst.insert(word)
        search_words = random.sample(best_ordered_sample, k=20)
        start = time.time_ns()
        for word in search_words:
            tst.search(word)
        end = time.time_ns()
        best_search_times[size] += (end - start)
    best_search_times[size] /= nr_runs * 1_000_000.0

    # ------------------------------------------
    # AVERAGE CASE: Random insertion
    # ------------------------------------------
    avg_sample = random.sample(words, k=size)

    insert_times[size] = 0.0
    for _ in range(nr_runs):
        tst = TernarySearchTree()
        start = time.time_ns()
        for word in avg_sample:
            tst.insert(word)
        end = time.time_ns()
        insert_times[size] += (end - start)
    insert_times[size] /= nr_runs * 1_000_000.0

    search_times[size] = 0.0
    for _ in range(nr_runs):
        tst = TernarySearchTree()
        for word in avg_sample:
            tst.insert(word)
        search_words = random.sample(avg_sample, k=20)
        start = time.time_ns()
        for word in search_words:
            tst.search(word)
        end = time.time_ns()
        search_times[size] += (end - start)
    search_times[size] /= nr_runs * 1_000_000.0

    # ------------------------------------------
    # WORST CASE: Sorted insertion (degenerate tree)
    # ------------------------------------------
    worst_ordered_sample = sorted(random.sample(words, k=size))

    worst_insert_times[size] = 0.0
    for _ in range(nr_runs):
        tst = TernarySearchTree()
        start = time.time_ns()
        for word in worst_ordered_sample:
            tst.insert(word)
        end = time.time_ns()
        worst_insert_times[size] += (end - start)
    worst_insert_times[size] /= nr_runs * 1_000_000.0

    worst_search_times[size] = 0.0
    for _ in range(nr_runs):
        tst = TernarySearchTree()
        for word in worst_ordered_sample:
            tst.insert(word)
        search_words = random.sample(worst_ordered_sample, k=20)
        start = time.time_ns()
        for word in search_words:
            tst.search(word)
        end = time.time_ns()
        worst_search_times[size] += (end - start)
    worst_search_times[size] /= nr_runs * 1_000_000.0

# -------------------------------
# PLOT: INSERTION TIME COMPARISON
# -------------------------------
plt.figure()
plt.plot(sizes, [insert_times[s] for s in sizes], label='Average Case', marker='o')
plt.plot(sizes, [best_insert_times[s] for s in sizes], label='Best Case', marker='^')
plt.plot(sizes, [worst_insert_times[s] for s in sizes], label='Worst Case', marker='s')
plt.title("TST Insert Time: Best vs Average vs Worst")
plt.xlabel("Number of words")
plt.ylabel("Insert Time (ms)")
plt.legend()
plt.grid(True)
plt.savefig("results/insert_cases_comparison.png")

# -------------------------------
# PLOT: SEARCH TIME COMPARISON
# -------------------------------
plt.figure()
plt.plot(sizes, [search_times[s] for s in sizes], label='Average Case', marker='o')
plt.plot(sizes, [best_search_times[s] for s in sizes], label='Best Case', marker='^')
plt.plot(sizes, [worst_search_times[s] for s in sizes], label='Worst Case', marker='s')
plt.title("TST Search Time: Best vs Average vs Worst")
plt.xlabel("Number of words")
plt.ylabel("Search Time (ms)")
plt.legend()
plt.grid(True)
plt.savefig("results/search_cases_comparison.png")

"""
------------------------------------------------------------------------------------------
Q6: Best, Average, and Worst Case Scenarios
------------------------------------------------------------------------------------------

Best Case:
- Tree is perfectly balanced, or words inserted in an order that keeps it balanced (e.g., median-first strategy).
- Insert/Search is O(L), fast traversal with minimal branching.

Average Case:
- Inserting words in random order (as done here) simulates a reasonably balanced tree.
- Insert/Search around O(L * log n).

Worst Case:
- Words are inserted in sorted or reverse sorted order.
- Tree becomes unbalanced and resembles a linked list.
- Insert/Search degrades to O(L * n).

In this benchmark:
- We use random word samples to approximate average-case performance.
- Best and worst-case scenarios are not explicitly simulated but could be tested by sorting the word list before insertion.
"""
