# Project concept data science

This repository contains the implementation of a ternary course tree in the concept of data science course at UHasselt. 
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

## What is it?

1. `benchmarking.py`: Python script for benchmarking.
1. `ternary_search_tree.ipynb`: Jupyter notebook for implementing the ternary search tree
1. `ternary_search_tree.py`: Python script for Ttreenode and TernarySearchTree classes

## Add: Explanation of how to work with the Ternary search Tree

## Conclusion summary
- 
