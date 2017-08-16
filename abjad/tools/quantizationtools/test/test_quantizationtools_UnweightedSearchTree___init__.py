import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_UnweightedSearchTree___init___01():

    search_tree = quantizationtools.UnweightedSearchTree()
    assert search_tree.definition == search_tree.default_definition


def test_quantizationtools_UnweightedSearchTree___init___02():

    definition = {2: None, 3: {2: None}}
    search_tree = quantizationtools.UnweightedSearchTree(definition)
    assert search_tree.definition == definition
