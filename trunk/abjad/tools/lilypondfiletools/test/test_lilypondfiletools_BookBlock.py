# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_BookBlock_01():

    book_block = lilypondfiletools.BookBlock()

    r'''
    \book {}
    '''

    assert book_block.lilypond_format == '\\book {}'
