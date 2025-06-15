"""Two classes, TtreeNode and TernarySearchTree to allow inserting and searching
words in a Ternary Search Tree framework"""


class TtreeNode:
    """A class for node objects belonging to a Ternary Search Tree
    Methods
    ----------
    all_strings : print all strings contained in the TST
    __len__     : return number of strings in the TST
    _to_string  :
    __repr__    : formatted string representation of TST
    _insert     : insert a string into the TST
    _psearch    : search TST for given prefix
    """
    
    def __init__(self, char: str):
        self.root = None
        self.string = None
        self._char = char  # value already stored in node x, store as attribute of this node
        self._lt, self._gt, self._eq = None, None, None  # less, equal, greater children
        self.flag_wordend = False  # mark the end of a word
        self.flag_empty = False  # mark empty string

    def _all_strings(self, pf=''):

        final_wordlist = []
        
        word = pf + self._char

        # if empty string was inserted: add to list
        if self.flag_empty:
            final_wordlist.append("")

        # if word was found: add to list
        if self.flag_wordend:
            final_wordlist.append(word)

        # traverse tree as long as children exist and no word end was found
        if self._lt is not None:
            final_wordlist.extend(self._lt._all_strings(pf))
        if self._gt is not None:
            final_wordlist.extend(self._gt._all_strings(pf))
        if self._eq is not None:
            # collect all words found and add to list
            words = self._eq._all_strings(word)
            final_wordlist.extend(words)

        return final_wordlist
    

    def __len__(self):
        """return length of search tree as number of inserted strings"""
        return len(self._all_strings())

    def _to_string(self, indent=' '):
        terminates = f'Terminates: {self.flag_wordend}'
        print_info = f'char: {repr(self)}, '
        repr_str = indent + print_info + indent + terminates
        if self._eq is not None:
            repr_str += '\n' + '_eq:' + self._eq._to_string(indent + '  ')
        if self._lt is not None:
            repr_str += '\n' + '_lt:' + self._lt._to_string(indent + '  ')
        if self._gt is not None:
            repr_str += '\n' + '_gt:' + self._gt._to_string(indent + '  ')
        return repr_str
    
    def __repr__(self):
        # star marks the end of a word
        return f"{self._char}{'*' if self.flag_wordend else ''}"
    
    def _insert(self, string):
        """ Recursive function to save characters from inserted words as ttree nodes
        Parameters
        ----------
        string : str

        Returns
        ----------
        
        """

        # mark empty string case
        if len(string) == 0:
            self.flag_empty = True

        else:
            char = string[0]
            if char < self._char:
                if self._lt is None:
                    self._lt = TtreeNode(char)
                self._lt._insert(string)  # always recurse

            elif char > self._char:
                if self._gt is None:
                    self._gt = TtreeNode(char)
                self._gt._insert(string)  # always recurse

            else:  # char == self._char
                if len(string) == 1:
                    self.flag_wordend = True
                else:
                    # if node with matched char was found:
                    # traverse tree
                    next_char = string[1]
                    if self._eq is None:
                        self._eq = TtreeNode(next_char)
                    self._eq._insert(string[1:])
   

    def _psearch(self, string):
        """given a node and a prefix string, search TST for its existence
        Parameters
        ----------
        string : str

        Returns
        ----------
        self or None
        """

        self.string = string

        if len(string) > 1:
            char = string[0]  # first character of search word
            rest = string[1::]
        else:
            char = string
            rest = string

        # if character is found:
        if char == self._char:
            if len(string) == 1:
                return self
            elif len(string) > 1:
                # traverse tree for string rest as long as children exist
                if self._eq is not None:
                    return self._eq._psearch(rest)
                else:
                    return None

        elif char < self._char:
            # traverse tree to look for a match
            if self._lt is not None:
                return self._lt._psearch(string)
            else:
                return None

        elif char > self._char:
            # traverse tree to look for a match
            if self._gt is not None:
                return self._gt._psearch(string)
            else:
                return None
        


class TernarySearchTree:
    """A class for a Ternary Search Tree object
        Methods
    ----------
    all_strings    : print all strings contained in the TST
    __len__        : return number of strings in the TST
    __repr__       : formatted string representation of TST
     insert        : insert a string into the TST
    prefix_search  : return wordlist of all strings in TST for given prefix
    search         : search for exact string or prefix in TST
    """
    
    def __init__(self):
        self._root = None


    def all_strings(self):
        """ return all strings stored in TST
        Parameters
        ----------
        
        Returns
        ----------
        List
        """
        if self._root is None:
            return []
        else:
            return self._root._all_strings()
        
    def __len__(self):
        if self._root is None:
            return 0
        else:
            return len(self._root)

    def __repr__(self):
        if self._root is None:
            return 'empty tree'
        else:
            return self._root._to_string('')

    def insert(self, string):
        """ insert a string into TST
        Parameters
        ----------
        string : str

        Returns
        ----------
        List
        """
        if self._root is None:
            # if empty string inserted: mark tree as non-empty
            if string == "":
                self._root = TtreeNode("*")
                self._root.flag_empty = True
                return
            else:
                # initiate tree
                self._root = TtreeNode(string[0])
        # recursive insertion of whole string
        self._root._insert(string)


    def prefix_search(self, node: TtreeNode, prefix):
        """ helper function for searching all words with given prefix
        Parameters
        ----------
        node    : TtreeNode
        prefix  : str
        
        Returns
        ----------
        List
        """
        if node._eq:
            # keep recursing into middle children as long as there is one
            # return all words that contain the prefix
            wordlist = node._eq._all_strings(prefix)
        elif node.flag_wordend:
            wordlist = [prefix]
        else:
            wordlist = []
        return wordlist
        


    def search(self, prefix, exact=False):
        """ method to search for words or prefixes
        Parameters
        ----------
        prefix  : str
        exact   : bool
        
        Returns
        ----------
        Boolean
        """
        # False if TST empty
        if self._root is None:
            return False
        
        # empty string is always a prefix
        if prefix == "":
            if self._root.flag_empty and exact:
                return True
        
        # traverse tree to search prefix
        node = self._root._psearch(prefix)
        # true if the empty prefix was inserted
        if prefix == "" and not exact:
            return True
        
        # prefix not found in tree
        if node is None:
            return False
        
        ## Exact string search ##
        if exact:
            if node.flag_wordend:
                return True
            else:
                return False

        ## Prefix string search ##
        elif not exact:
            # search for all words containing the prefix
            wordlist = self.prefix_search(node, prefix)
            if wordlist:
                return True
            return False

