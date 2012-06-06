from abjad.tools.lilypondfiletools.NonattributedBlock import NonattributedBlock


class BookBlock(NonattributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file book block::

        >>> book_block = lilypondfiletools.BookBlock()

    ::

        >>> book_block
        BookBlock()

    ::

        >>> f(book_block)
        \book {}

    Return book block.
    '''

    def __init__(self):
        NonattributedBlock.__init__(self)
        self._escaped_name = r'\book'
        self._is_formatted_when_empty = True
