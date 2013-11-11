# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_BookBlock_01():

    book_block = lilypondfiletools.BookBlock()

    assert systemtools.TestManager.compare(
        book_block,
        r'''
        \book {}
        '''
        )
