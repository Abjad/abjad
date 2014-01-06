# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.Block import Block


class BookpartBlock(Block):
    r'''Abjad model of LilyPond input file bookpart block:

    ::

        >>> bookpart_block = lilypondfiletools.BookpartBlock()

    ::

        >>> bookpart_block
        BookpartBlock()

    ..  doctest::

        >>> print format(bookpart_block)
        \bookpart {}

    '''

    def __init__(self):
        Block.__init__(self, name='bookpart')
        #self._escaped_name = r'\bookpart'
