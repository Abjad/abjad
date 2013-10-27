# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_BookpartBlock_01():

    bookpart_block = lilypondfiletools.BookpartBlock()

    r'''
    \bookpart {}
    '''

    assert bookpart_block.lilypond_format == '\\bookpart {}'
