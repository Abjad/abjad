# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock


class BookpartBlock(AttributedBlock):
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
        AttributedBlock.__init__(self)
        self._escaped_name = r'\bookpart'
