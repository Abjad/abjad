from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock


class HeaderBlock(AttributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file header block::

        >>> header_block = lilypondfiletools.HeaderBlock()

    ::

        >>> header_block
        HeaderBlock()

    ::

        >>> header_block.composer = markuptools.Markup('Josquin')
        >>> header_block.title = markuptools.Markup('Missa sexti tonus')

    ::

        >>> f(header_block)
        \header {
            composer = \markup { Josquin }
            title = \markup { Missa sexti tonus }
        }

    Return header block.
    '''

    def __init__(self):
        AttributedBlock.__init__(self)
        self._escaped_name = r'\header'
