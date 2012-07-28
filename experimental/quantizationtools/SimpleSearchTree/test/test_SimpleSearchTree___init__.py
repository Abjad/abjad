from experimental import quantizationtools


def test_SimpleSearchTree___init___01():

    search_tree = quantizationtools.SimpleSearchTree()
    assert search_tree.definition == search_tree.default_definition


def test_SimpleSearchTree___init___02():

    definition = {2: None, 3: {2: None}}
    search_tree = quantizationtools.SimpleSearchTree(definition)
    assert search_tree.definition == definition
    
