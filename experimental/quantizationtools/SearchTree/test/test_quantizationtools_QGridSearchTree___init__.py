import py.test
from experimental.quantizationtools import SearchTree


def test_quantizationtools_QGridSearchTree___init___01():
    '''SearchTree is instantiated from a dict.'''
    definition = {2: {2: None, 3: None}, 5: None}
    qst = SearchTree(definition)
    assert qst == definition


def test_quantizationtools_QGridSearchTree___init___02():
    '''Definition may not contain non-primes.'''
    definition = {4: None}
    assert py.test.raises(ValueError, 'qst = SearchTree(definition)')


def test_quantizationtools_QGridSearchTree___init___03():
    '''Without arguments, default to Nauert's pruned search tree.'''
    qst = SearchTree()
    assert qst == {
        2: {2: {2: {2: None}, 3: None}, 3: None, 5: None, 7: None},
        3: {2: {2: None}, 3: None, 5: None},
        5: {2: None, 3: None},
        7: {2: None},
        11: None,
        13: None
    }
