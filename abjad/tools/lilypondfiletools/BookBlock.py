# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock


class BookBlock(AttributedBlock):
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
        AttributedBlock.__init__(self)
        self._escaped_name = r'\book'
