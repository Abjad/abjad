from abjad import *
from abjad.tools import sequencetools


def test_Tree__storage_format_01():
    '''Placeholder test to remind that tree storage format should recursively indent.
    '''
    
    tree = sequencetools.Tree([[0, 1, 2], [3], [4, 5]])

    # TODO: make ouput fully recursif (and so indentented at more levels than just 1)
    r'''
    sequencetools.Tree(
        [[0, 1, 2], [3], [4, 5]]
        )
    '''

    assert tree._storage_format == 'sequencetools.Tree(\n\t[[0, 1, 2], [3], [4, 5]]\n\t)'
