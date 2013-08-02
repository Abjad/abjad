# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.NonattributedBlock \
	import NonattributedBlock


class BookpartBlock(NonattributedBlock):
    r'''Abjad model of LilyPond input file bookpart block:

    ::

        >>> bookpart_block = lilypondfiletools.BookpartBlock()

    ::

        >>> bookpart_block
        BookpartBlock()

    ..  doctest::

        >>> f(bookpart_block)
        \bookpart {}

    Return bookpart block.
    '''

    def __init__(self):
        NonattributedBlock.__init__(self)
        self._escaped_name = r'\bookpart'
        self._is_formatted_when_empty = True
