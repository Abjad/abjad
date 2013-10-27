# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.NonattributedBlock \
	import NonattributedBlock


class BookBlock(NonattributedBlock):
    r'''Abjad model of LilyPond input file book block:

    ::

        >>> book_block = lilypondfiletools.BookBlock()

    ::

        >>> book_block
        BookBlock()

    ..  doctest::

        >>> f(book_block)
        \book {}

    Returns book block.
    '''

    def __init__(self):
        NonattributedBlock.__init__(self)
        self._escaped_name = r'\book'
        self._is_formatted_when_empty = True
