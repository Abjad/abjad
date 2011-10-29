from abjad import *


def test_scoretools_make_piano_sketch_staff_from_leaves_01():

    notes = notetools.make_notes([-12, -10, -8, -7, -5, 0, 2, 4, 5, 7], [(1, 4)])
    score, treble_staff, bass_staff = scoretools.make_piano_sketch_score_from_leaves(notes)

    r'''
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
    '''

    assert score.format == '\\new Score \\with {\n\t\\override BarLine #\'stencil = ##f\n\t\\override BarNumber #\'transparent = ##t\n\t\\override SpanBar #\'stencil = ##f\n\t\\override TimeSignature #\'stencil = ##f\n} <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t\t#(set-accidental-style \'forget)\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tc\'4\n\t\t\td\'4\n\t\t\te\'4\n\t\t\tf\'4\n\t\t\tg\'4\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t\t#(set-accidental-style \'forget)\n\t\t\tc4\n\t\t\td4\n\t\t\te4\n\t\t\tf4\n\t\t\tg4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t}\n\t>>\n>>'
