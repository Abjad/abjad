from abjad import *


def test_Tree__storage_format_01():
    '''Placeholder test to remind that tree storage format should recursively indent.
    '''
    
    tree = sequencetools.Tree([[0, 1, 2], [3], [4, 5]])

    # TODO: make ouput fully recursive (and so indentented at more levels than just 1)
    r'''
    sequencetools.Tree(
        [0, 1, 2],
        [3],
        [4, 5]
        )
    '''

    assert tree.storage_format == 'sequencetools.Tree(\n\t[0, 1, 2],\n\t[3],\n\t[4, 5]\n\t)'
