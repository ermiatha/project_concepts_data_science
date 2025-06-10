"""Two classes, TtreeNode and TernarySearchTree to allow inserting and searching
words in a Ternary Search Tree framework"""


class TtreeNode:
    """A class for node objects belonging to a Ternary Search Tree"""
    
    def __init__(self, char):
        self.root = None
        self.string = None
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
        """given a node and a prefix string, search Tree for its existence"""
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
                    #print('found new path?')
                    return self._eq._psearch(rest)
                else:
                    #print('correctly found last word node')
                    return None

        elif char < self._char:
            if self._lt is not None:
                return self._lt._psearch(string)
            else:
                return None

        elif char > self._char:
            if self._gt is not None:
                return self._gt._psearch(string)
            else:
                return None
        
        print("no condition matched yet: now return none")


class TernarySearchTree:
    """A class for a Ternary Search Tree object"""
    
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



    def search(self, prefix, exact=False):
        """method to search for words or prefixes"""
        if self._root is None:
            return False
        
        node = self._root._psearch(prefix)

        if node is None:
            return []
        
        # if we search for exact word
        if exact:
            if node.flag_wordend:
                return [prefix]
            else:
                return []

        # if we search for a prefix
        elif not exact: 
            if node._eq:
                # keep recursing into middle children as long as there is one
                # return all words that contain the prefix
                return node._eq._all_strings(prefix)
            elif node.flag_wordend:
                return [prefix]
            else:
                return node


"""
------------------------------------------------------------------------------------------
Q4: Time and Space Complexity of Ternary Search Tree (TST)
------------------------------------------------------------------------------------------

Time Complexity (n = number of words, L = average word length):

- Insertion:
    - Worst Case: O(L * n) → if the tree becomes unbalanced (like a linked list)
    - Average Case: O(L * log n) → assuming a roughly balanced ternary tree
    - Best Case: O(L) → for inserting words into an optimally balanced TST

- Search:
    - Worst Case: O(L * n) → in a degenerate (unbalanced) tree
    - Average Case: O(L * log n)
    - Best Case: O(L)

- Prefix Search:
    - TST supports prefix search naturally and efficiently in O(L) time (to find prefix) + O(k) to collect matching strings.

Space Complexity:

- O(n * L), where:
    - n = number of distinct words
    - L = average length of each word
    - Each character may be stored in a separate node, but space is reused for common prefixes.
- Additional memory for three pointers (left, mid, right) per node.

Comparison:
- Python's set() has O(1) average insert and search time using hash tables, but does not support prefix search.
- TST trades off speed for space efficiency and support for prefix queries.
"""