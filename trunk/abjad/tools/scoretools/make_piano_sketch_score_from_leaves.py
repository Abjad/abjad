from abjad.tools import contexttools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools.pitchtools import NamedChromaticPitch
from abjad.tools.scoretools.make_piano_score_from_leaves import make_piano_score_from_leaves


def make_piano_sketch_score_from_leaves(leaves, lowest_treble_pitch = NamedChromaticPitch('b')):
    r'''.. versionadded:: 2.0

    Make piano sketch score from `leaves`::

        abjad> notes = notetools.make_notes([-12, -10, -8, -7, -5, 0, 2, 4, 5, 7], [(1, 4)])
        abjad> score, treble_staff, bass_staff = scoretools.make_piano_sketch_score_from_leaves(notes)

    ::

        abjad> f(score)
        \new Score \with {
            \override BarLine #'stencil = ##f
            \override BarNumber #'transparent = ##t
            \override SpanBar #'stencil = ##f
            \override TimeSignature #'stencil = ##f
        } <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                    #(set-accidental-style 'forget)
                    r4
                    r4
                    r4
                    r4
                    r4
                    c'4
                    d'4
                    e'4
                    f'4
                    g'4
                }
                \context Staff = "bass" {
                    \clef "bass"
                    #(set-accidental-style 'forget)
                    c4
                    d4
                    e4
                    f4
                    g4
                    r4
                    r4
                    r4
                    r4
                    r4
                }
            >>
        >>

    Make time signatures and bar numbers transparent.

    Do not print bar lines or span bars.

    Set all staff accidental styles to forget.

    Return score, treble staff, bass staff.
    '''

    # make and configure score
    score, treble_staff, bass_staff = make_piano_score_from_leaves(leaves, lowest_treble_pitch)
    score.override.time_signature.stencil = False
    score.override.bar_number.transparent = True
    score.override.bar_line.stencil = False
    score.override.span_bar.stencil = False
    contexttools.set_accidental_style_on_sequential_contexts_in_expr(score, 'forget')

    # make and configure lily file
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    lilypond_file.layout_block.indent = 0
    lilypond_file.paper_block.tagline = markuptools.Markup('')

    # return score, treble staff, bass staff
    return score, treble_staff, bass_staff
