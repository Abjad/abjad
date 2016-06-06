# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import override


def make_piano_sketch_score_from_leaves(leaves, lowest_treble_pitch=None):
    r'''Make piano sketch score from `leaves`:

    ::

        >>> notes = scoretools.make_notes(
        ...     [-12, -10, -8, -7, -5, 0, 2, 4, 5, 7],
        ...     [(1, 16)],
        ...     )
        >>> score, treble_staff, bass_staff = \
        ...     scoretools.make_piano_sketch_score_from_leaves(notes)

    ..  doctest::

        >>> print(format(score))
        \new Score \with {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        } <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                    r16
                    r16
                    r16
                    r16
                    r16
                    c'16
                    d'16
                    e'16
                    f'16
                    g'16
                }
                \context Staff = "bass" {
                    \clef "bass"
                    c16
                    d16
                    e16
                    f16
                    g16
                    r16
                    r16
                    r16
                    r16
                    r16
                }
            >>
        >>

    ::

        >>> show(score) # doctest: +SKIP

    When ``lowest_treble_pitch=None`` set to B3.

    Make time signatures and bar numbers transparent.

    Do not print bar lines or span bars.

    Returns score, treble staff, bass staff.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import lilypondfiletools
    from abjad.tools import markuptools
    from abjad.tools import pitchtools
    from abjad.tools import scoretools

    if lowest_treble_pitch is None:
        lowest_treble_pitch = pitchtools.NamedPitch('b')

    # make and configure score
    score, treble_staff, bass_staff = \
        scoretools.make_piano_score_from_leaves(leaves, lowest_treble_pitch)
    override(score).time_signature.stencil = False
    override(score).bar_number.transparent = True
    override(score).bar_line.stencil = False
    override(score).span_bar.stencil = False

    # make and configure lily file
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    lilypond_file.layout_block.indent = 0
    lilypond_file.paper_block.tagline = markuptools.Markup('')

    # return score, treble staff, bass staff
    return score, treble_staff, bass_staff
