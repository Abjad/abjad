from abjad import *


def test_BookpartBlock_01():

    bookpart_block = lilypondfiletools.BookpartBlock()

    r'''
    \bookpart {}
    '''

    assert bookpart_block.format == '\\bookpart {}'
