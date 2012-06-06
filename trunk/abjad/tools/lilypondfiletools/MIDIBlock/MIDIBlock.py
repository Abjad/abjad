from abjad.tools.lilypondfiletools.AttributedBlock import AttributedBlock


class MIDIBlock(AttributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file MIDI block::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> score = Score([staff])
        >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)

    ::

        >>> lilypond_file.score_block.append(lilypondfiletools.MIDIBlock())

    ::

        >>> layout_block = lilypondfiletools.LayoutBlock()
        >>> layout_block.is_formatted_when_empty = True
        >>> lilypond_file.score_block.append(layout_block)

    ::

        >>> f(lilypond_file.score_block)
        \score {
            \new Score <<
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>
            \midi {}
            \layout {}
        }

    MIDI blocks are formatted even when they are empty.

    The example here appends MIDI and layout blocks to a score block.
    Doing this allows LilyPond to create both MIDI and PDF output
    from a single input file.

    Read the LilyPond docs on LilyPond file structure for the details
    as to why this is the case.
    '''

    def __init__(self):
        AttributedBlock.__init__(self)
        self._escaped_name = r'\midi'
        self.is_formatted_when_empty = True
