# Project in 'Concepts of Data Ccience': A Ternary Search Tree Implementation

This repository contains the implementation, testing and benchmarking of a Ternary Search Tree in the 'Concepts of Data Science' course at UHasselt. 
The students are Luong Vuong (2365900) and Ermioni Athanasiadi (2365990)

## Project Structure

```
├── data/ # input datasets for testing and benchmarking
│   ├── README.md
│   └── search_trees/
│       ├── corncob_lowercase.txt
│       ├── insert_words.txt
│       ├── insert_words_test.txt
│       ├── not_insert_words.txt
│       ├── README.md
│       └── .ipynb_checkpoints/
│           ├── insert_words-checkpoint.txt
│           └── not_insert_words-checkpoint.txt
├── results/ # benchmarking visualizations
│   ├── insert_comparison.png
│   ├── search_comparison.png
│   ├── insert_tst.png
│   └── search_tst.png
├── benchmarking.py # script to run benchmarking
├── benchmarking.slurm # SLURM job script for HPC runs
├── ternary_search_tree.py # TST implementation
├── ternary_search_tree.ipynb # Jupyter notebook to demonstrate working with tree
├── slurm-*.out # output logs from HPC jobs
├── .gitignore
└── README.md # project documentation
```


---

## What is included?
- A recursive Ternary Search Tree implementation
- Support for string insertion, exact match, prefix-based search and all-strings retrieval
- Benchmarking results with summary and visualizations
- SLURM-compatibility for HPC environments

1. `benchmarking.py`: Python script for benchmarking.
2. `ternary_search_tree.ipynb`: Jupyter notebook for implementing the ternary search tree
3. `ternary_search_tree.py`: Python script for Ttreenode and TernarySearchTree classes

---

## Quick Start

### Installation

You need Python and Jupyter Notebook. You can install further dependencies with:

```bash
pip install numpy matplotlib random time
```

### Example Usage
```python
from ternary_search_tree import TernarySearchTree

tst = TernarySearchTree()

# insert words into the tree
words = ["cat", "car", "cart", "care", "fly", ""]

for word in words:
    tst.insert(word)

# search for an exact match
print(tst.search("cat", exact=True))    # True
print(tst.search("cats", exact=True))   # False

# prefix search
print(tst.search("ca"))                 # True (matches 'cat', 'car', 'cart', 'care')

# search for empty string
print(tst.search("", exact=True))       # True because inserted
print(tst.search(""))                   # always True because "" is prefix of all strings

# Get all inserted strings
print(tst.all_strings())                # ['', 'fly', 'cat', 'car', 'cart', 'care']
```

### How to Run Benchmarks
#### Locally
```bash
python benchmarking.py
```
#### On HPC (SLURM)
```bash
sbatch benchmarking.slurm
```

## Conclusion summary: Performance and Practical Use of Ternary Search Trees (TSTs)
Ternary Search Trees (TSTs) offer a flexible data structure for storing and and searching of strings, particularly when dealing with large sets of similar or prefix-sharing words.

### Insertion Performance
- **Scalability:** Insertion time follows a more or less linear trend with respect to the number of inserted words. No recursion errors were encountered in our benchmarks (up to 50,000 words), but such errors are expected for larger datasets due to the recursive nature of the implementation.
- **Input Order Matters:** Insertion performance varies with input order:
  - Random and explicitly balanced insertions show similar performance, indicating that TSTs naturally form reasonably balanced structures when words are inserted in random order.
  - Inserting sorted word lists creates long, unbalanced branches, significantly degrading performance due to deep recursion and many redundant comparisons.

### Search Performance
- **Prefix vs. Exact Search:**
  - Prefix-based search is flexible but requires traversing all possible continuations, which quickly becomes costly in large TST's.
  - Exact match searches are faster, because the TST benefits from early termination, and avoids the traversal of multiple branches, unlike in prefix searches.
- **Performance Comparison:** 
  - Search performance is reasonable but **significantly slower** than Python’s built-in `set()` type for exact matches, which benefits from hash table optimizations.
  - Median and random case searches behave similarly in TSTs.
  - **Worst-case scenarios** (e.g., searching in a tree built from a sorted list) are of course more expensive, as the tree becomes very deep and all nodes along a branch may need to be visited.

###  Limitations
- The current recursive implementation limits scalability, particularly with large datasets, due to Python’s recursion depth limit.
- TSTs were not benchmarked on datasets larger than ~50,000 words. Practical use on significantly larger datasets would request an iterative or tail-recursive implementation.

### Alternatives and Trade-offs
- **Python `set`** are highly efficient and outperformed our TST in all comparisons. They are fast for exact matches but lack built-in support for prefix queries or lexicographic traversal.
- **Binary Search Trees (BSTs)** were not compared with TST's , but can be used for string storage and may offer better balancing with self-balancing variants (e.g., AVL, Red-Black Trees), but are less suited for prefix-based queries without extra logic.
- **Tries (Prefix Trees)** could be an interesting option to consider for prefix lookups and often faster than TSTs in such tasks. It may be, however, that they consume more memory for sparse datasets or shorter words.
