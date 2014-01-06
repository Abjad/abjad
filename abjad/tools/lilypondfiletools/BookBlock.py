# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.Block import Block


class BookBlock(Block):
    r'''Abjad model of LilyPond input file book block:

    ::

        >>> book_block = lilypondfiletools.BookBlock()

    ::

        >>> book_block
        BookBlock()

    ..  doctest::

        >>> print format(book_block)
        \book {}

    '''

    def __init__(self):
        Block.__init__(self, name='book')
        #self._escaped_name = r'\book'
