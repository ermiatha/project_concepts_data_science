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

## Conclusion summary
- 
