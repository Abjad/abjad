from abjad import *


def test_BookBlock_01():

    book_block = lilypondfiletools.BookBlock()

    r'''
    \book {}
    '''

    assert book_block.format == '\\book {}'
