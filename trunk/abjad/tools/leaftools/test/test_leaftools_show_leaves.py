from abjad import *


def test_leaftools_show_leaves_01():

    leaves = leaftools.make_leaves([None, 1, (-24, -22, 7, 21), None], (1, 4))
    score = leaftools.show_leaves(leaves, suppress_pdf = True)

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
                cs'4
                <g' a''>4
                r4
            }
            \context Staff = "bass" {
                \clef "bass"
                #(set-accidental-style 'forget)
                r4
                r4
                <c, d,>4
                r4
            }
        >>
    >>
    '''

    assert componenttools.is_well_formed_component(score)
    assert score.format == '\\new Score \\with {\n\t\\override BarLine #\'stencil = ##f\n\t\\override BarNumber #\'transparent = ##t\n\t\\override SpanBar #\'stencil = ##f\n\t\\override TimeSignature #\'stencil = ##f\n} <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t\t#(set-accidental-style \'forget)\n\t\t\tr4\n\t\t\tcs\'4\n\t\t\t<g\' a\'\'>4\n\t\t\tr4\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t\t#(set-accidental-style \'forget)\n\t\t\tr4\n\t\t\tr4\n\t\t\t<c, d,>4\n\t\t\tr4\n\t\t}\n\t>>\n>>'
