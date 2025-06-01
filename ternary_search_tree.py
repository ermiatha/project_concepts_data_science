class TtreeNode:
    
    def __init__(self, char):
        self.root = None
        self.string = None
        #self._word = char  # to store in list of all words?
        self._char = char[0]  # value already stored in node x, store as attribute of this node
        self._lt, self._gt, self._eq = None, None, None
        self.flag_wordend = False  # mark the end of a word

    def _all_strings(self, pf=''):
        #print(f'printing {self} with prefix {pf}')
        final_wordlist = []
        
        word = pf + self._char

        # missing: if prefix empty, add it as word

        if self.flag_wordend:
            final_wordlist.append(word)

        if self._lt is not None:
            #print(self._lt)
            final_wordlist.extend(self._lt._all_strings(pf))
        if self._gt is not None:
            #print(self._gt)
            final_wordlist.extend(self._gt._all_strings(pf))
        if self._eq is not None:
            #print(self._eq)
            words = self._eq._all_strings(word)
            final_wordlist.extend(words)

        return final_wordlist
    
    def __len__(self):
        # should count keys, not nodes
        if self.flag_wordend:
            length = 1
        else:
            length = 0
        # add edge case if string is empty
        # if self._char == "":
        #     length += 1

        if self._eq is not None:
                length += len(self._eq)
        if self._lt is not None:
                length += len(self._lt)
        if self._gt is not None:
                length += len(self._gt)
        
        return length

    def _to_string(self, indent=' '):
        terminates = f'Terminates: {self.flag_wordend}'
        print_info = f'char: {repr(self)}, '
        #repr_str = indent + repr(self)
        repr_str = indent + print_info + indent + terminates
        if self._eq is not None:
            repr_str += '\n' + '_eq:' + self._eq._to_string(indent + '  ')
        if self._lt is not None:
            repr_str += '\n' + '_lt:' + self._lt._to_string(indent + '  ')
        if self._gt is not None:
            repr_str += '\n' + '_gt:' + self._gt._to_string(indent + '  ')
        return repr_str
    
    def __repr__(self):
        # remove star later, for now just for debugging
        return f"{self._char}{'*' if self.flag_wordend else ''}"
    
    def _insert(self, string):
        #print(f'inserting {string} at node {self._char}')
        # string is the new key to insert
        # self.string is the value already stored in this node,  holds the current key in this node
        self.string = string  # only the first time the function is called -> add flag as function argument
        
        if len(string) > 0:
            char = string[0]  # first character of new word
            rest = string[1::]  # if rest as list: char, *rest = string
        else:
            char = string
            rest = string

        # if string contains more than one character
        if len(string) > 1:
            # character matches
            if char == self._char:

            # insert in middle child
                if self._eq is None:
                    self._eq = TtreeNode(rest[0])
                self._eq._insert(rest)

            # if earlier in the alphabet:
            elif char < self._char:
                if self._lt is None:
                    self._lt = TtreeNode(char)
                self._lt._insert(string)
            # if later in the alphabet
            elif char > self._char:
                if self._gt is None:
                    self._gt = TtreeNode(char)
                self._gt._insert(string)
        #elif string == "":
        #    if self._eq is None:
        #        self._eq = TtreeNode(string)
        #    self._eq._insert(string)
        else:
            self.flag_wordend = True
        
        return string
    
    def _psearch(self, string):
        self.string = string
        #print(self._char)

        if len(string) > 1:
            char = string[0]  # first character of search word
            rest = string[1::]
        else:  # necessary?
            char = string
            rest = string
        
        print(f'searching for char {char} at node {self._char}')

        # if character is found:
        if char == self._char:
            if len(string) == 1:
                return self
            elif len(string) > 1:
                if self._eq is not None:
                    return self._eq._psearch(rest)

        elif char < self._char:
            if self._lt is not None:
                return self._lt._psearch(string)

        elif char > self._char:
            if self._gt is not None:
                return self._gt._psearch(string)


class TernarySearchTree:
    
    def __init__(self):
        self._root = None

    def all_strings(self):
        if self._root is None:
            return []
        else:
            return self._root._all_strings()
        
    def __len__(self):
        print(f'printing length of {self._root}')
        if self._root is None:
            return 0
        else:
            return len(self._root)
    
    def __repr__(self):
        if self._root is None:
            return 'empty tree'
        else:
            #print("print string here")
            return self._root._to_string('')
    
    def insert(self, string):
        if self._root is None:
            #print(f'inserting {string} at node {self._root}')
            self._root = TtreeNode(string)
        self._root._insert(string)


    def search(self, prefix):
        if self._root is None:
            return False
        node = self._root._psearch(prefix)
        #print(node)
        if node is None:
            return []
        elif node._eq:
            # keep recursing into middle children as long as there is one
            # return all words that contain the prefix
            return node._eq._all_strings(prefix)
        elif node.flag_wordend:
            return [prefix]
        else:
            return node

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
