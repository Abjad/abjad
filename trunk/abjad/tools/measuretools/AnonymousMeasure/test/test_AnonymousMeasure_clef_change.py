from abjad import *


def test_AnonymousMeasure_clef_change_01():
    '''Clef sequence: treble, bass, treble.
    Important that measure three format *only bass clef*.
    If measure three format treble *and* bass clef, there's contention.
    Contention as to whether leaf or measure should format clef.'''

    t = Staff([])
    t.append(measuretools.AnonymousMeasure("c'8 d'8"))
    contexttools.ClefMark('treble')(t)
    t.append(measuretools.AnonymousMeasure("c'8 d'8"))
    contexttools.ClefMark('bass')(t[-1])
    t.append(measuretools.AnonymousMeasure("c'8 d'8"))
    contexttools.ClefMark('treble')(t[-1])

    r'''
    \new Staff {
        {
            \override Staff.TimeSignature #'stencil = ##f
            \clef "treble"
            \time 1/4
            c'8
            d'8
            \revert Staff.TimeSignature #'stencil
        }
        {
            \override Staff.TimeSignature #'stencil = ##f
            \clef "bass"
            \time 1/4
            c'8
            d'8
            \revert Staff.TimeSignature #'stencil
        }
        {
            \override Staff.TimeSignature #'stencil = ##f
            \clef "treble"
            \time 1/4
            c'8
            d'8
            \revert Staff.TimeSignature #'stencil
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Staff {\n\t\\clef "treble"\n\t{\n\t\t\\override Staff.TimeSignature #\'stencil = ##f\n\t\t\\time 1/4\n\t\tc\'8\n\t\td\'8\n\t\t\\revert Staff.TimeSignature #\'stencil\n\t}\n\t{\n\t\t\\override Staff.TimeSignature #\'stencil = ##f\n\t\t\\clef "bass"\n\t\t\\time 1/4\n\t\tc\'8\n\t\td\'8\n\t\t\\revert Staff.TimeSignature #\'stencil\n\t}\n\t{\n\t\t\\override Staff.TimeSignature #\'stencil = ##f\n\t\t\\clef "treble"\n\t\t\\time 1/4\n\t\tc\'8\n\t\td\'8\n\t\t\\revert Staff.TimeSignature #\'stencil\n\t}\n}'
