import py.test
from abjad.tools.quantizationtools import QGridSearchTree


def test_quantizationtools_QGridSearchTree___new___01():
    '''QGridSearchTree is instantiated from a dict.'''
    definition = {2: {2: None, 3: None}, 5: None}
    qst = QGridSearchTree(definition)
    assert qst == definition


def test_quantizationtools_QGridSearchTree___new___02():
    '''Definition may not contain non-primes.'''
    definition = {4: None}
    assert py.test.raises(ValueError, 'qst = QGridSearchTree(definition)')


def test_quantizationtools_QGridSearchTree___new___03():
    '''Without arguments, default to Nauert's pruned search tree.'''
    qst = QGridSearchTree()
    assert qst == {
        2: {2: {2: {2: None}, 3: None}, 3: None, 5: None, 7: None},
        3: {2: {2: None}, 3: None, 5: None},
        5: {2: None, 3: None},
        7: {2: None},
        11: None,
        13: None
    }
