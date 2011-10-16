from abjad.tools.lilypondfiletools._AttributedBlock import _AttributedBlock


class HeaderBlock(_AttributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file header block::

        abjad> header_block = lilypondfiletools.HeaderBlock()

    ::

        abjad> header_block
        HeaderBlock()

    ::

        abjad> header_block.composer = markuptools.Markup('Josquin')
        abjad> header_block.title = markuptools.Markup('Missa sexti tonus')

    ::

        abjad> f(header_block)
        \header {
            composer = \markup { Josquin }
            title = \markup { Missa sexti tonus }
        }

    Return header block.
    '''

    def __init__(self):
        _AttributedBlock.__init__(self)
        self._escaped_name = r'\header'
