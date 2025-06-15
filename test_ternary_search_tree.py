import pytest
from ternary_search_tree import TernarySearchTree

# _____________ Fixing _____________

@pytest.fixture
def inserted_words():
    with open('data/search_trees/insert_words.txt') as file:
        return [line.strip() for line in file]

@pytest.fixture
def not_inserted_words():
    with open('data/search_trees/not_insert_words.txt') as file:
        return [line.strip() for line in file]

@pytest.fixture
def tst(inserted_words):
    tree = TernarySearchTree()
    for word in inserted_words:
        tree.insert(word)
    return tree

@pytest.fixture
def unique_inserted_words(inserted_words):
    return set(inserted_words)

# _____________ Testing _____________

def test_tree_length_matches_inserted_words(tst, unique_inserted_words):
    assert len(tst) == len(unique_inserted_words), \
        f'{len(tst)} in tree, expected {len(unique_inserted_words)}'

def test_all_inserted_words_found(tst, unique_inserted_words):
    for word in unique_inserted_words:
        assert tst.search(word), f'{word} not found'

def test_prefix_searches_work(tst, unique_inserted_words):
    for word in unique_inserted_words:
        for i in range(len(word) - 1, 0, -1):
            prefix = word[:i]
            assert tst.search(prefix), f'{prefix} not found'

def test_exact_search_matches_only_full_words(tst, unique_inserted_words):
    for word in unique_inserted_words:
        for i in range(len(word), 0, -1):
            prefix = word[:i]
            if prefix not in unique_inserted_words:
                assert not tst.search(prefix, exact=True), \
                    f'{prefix} should not be found (exact=True)'


# _____________ Edge Case Testing _____________

def test_empty_string_behavior(tst):
    # "" is considered a prefix of all, but not exactly present unless explicitly inserted
    assert tst.search(''), 'empty string not found (as prefix)'
    assert not tst.search('', exact=True), 'empty string should not be found as exact match'

def test_words_not_inserted_are_not_found(tst, not_inserted_words):
    for word in not_inserted_words:
        assert not tst.search(word), f'{word} should not be found'

def test_all_strings_returned(tst, unique_inserted_words):
    all_strings = tst.all_strings()
    assert len(all_strings) == len(unique_inserted_words), \
        f'{len(all_strings)} words, expected {len(unique_inserted_words)}'
    assert sorted(all_strings) == sorted(unique_inserted_words), 'word lists do not match'


# _____________ Detailed Testing _____________
@pytest.mark.parametrize("insert_words, search_word, exact, expected", [
    (["", "b"], "", False, True),                           # prefix search finds inserted empty string
    (["", "b"], "", True, True),                            # exact search finds inserted empty string
    (["b"], "", True, False),                               # exact search does not find not-inserted empty string
    (["b"], "", False, True),                               # prefix search finds not-inserted empty string
    (["abc", "cat", "a", "", "b"], "abc", None, True),      # prefix search found when exact is present; None = default, i.e. exact=False assumed
    (["abc", "cat", "a", "", "b"], "a", True, True),        # exact 1-char word is found
    (["abc", "cat", "a", "", "b"], "ac", None, False),      # exact non-inserted word is not found
])
def test_insert_and_search_cases(insert_words, search_word, exact, expected):
    tree = TernarySearchTree()
    for word in insert_words:
        tree.insert(word)

    if exact is None:
        result = tree.search(search_word)
    else:
        result = tree.search(search_word, exact=exact)

    assert result is expected