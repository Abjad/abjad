# -*- encoding: utf-8 -*-
from abjad import *


def test_PayloadTree__storage_format_01():
    r'''Placeholder test to remind that tree storage format should recursively indent.
    '''

    tree = sequencetools.PayloadTree([[0, 1, 2], [3], [4, 5]])

    # TODO: make ouput fully recursive (and so indentented at more levels than just 1)
    r'''
    sequencetools.PayloadTree(
        [0, 1, 2],
        [3],
        [4, 5]
        )
    '''

    assert tree.storage_format == 'sequencetools.PayloadTree(\n\t[[0, 1, 2], [3], [4, 5]]\n\t)'
