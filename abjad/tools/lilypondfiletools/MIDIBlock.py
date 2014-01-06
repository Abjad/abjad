# -*- encoding: utf-8 -*-
from abjad.tools.lilypondfiletools.Block import Block


class MIDIBlock(Block):
    r'''Abjad model of LilyPond input file MIDI block:

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> score = Score([staff])
        >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)

    ::

        >>> lilypond_file.score_block.items.append(lilypondfiletools.MIDIBlock())

    ::

        >>> layout_block = lilypondfiletools.LayoutBlock()
        >>> lilypond_file.score_block.items.append(layout_block)

    ..  doctest::

        >>> print format(lilypond_file.score_block)
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
        Block.__init__(self)
        self._escaped_name = r'\midi'
