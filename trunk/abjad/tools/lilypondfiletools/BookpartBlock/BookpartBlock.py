from abjad.tools.lilypondfiletools._NonattributedBlock import _NonattributedBlock


class BookpartBlock(_NonattributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file bookpart block::

        abjad> bookpart_block = lilypondfiletools.BookpartBlock()

    ::

        abjad> bookpart_block
        BookpartBlock()

    ::

        abjad> f(bookpart_block)
        \bookpart {}

    Return bookpart block.
    '''

    def __init__(self):
        _NonattributedBlock.__init__(self)
        self._escaped_name = r'\bookpart'
        self._is_formatted_when_empty = True
