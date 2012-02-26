from abjad.tools.lilypondfiletools._NonattributedBlock import _NonattributedBlock


class BookBlock(_NonattributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file book block::

        abjad> book_block = lilypondfiletools.BookBlock()

    ::

        abjad> book_block
        BookBlock()

    ::

        abjad> f(book_block)
        \book {}

    Return book block.
    '''

    def __init__(self):
        _NonattributedBlock.__init__(self)
        self._escaped_name = r'\book'
        self._is_formatted_when_empty = True
