from abjad import *


def test_AnonymousMeasure_duration_interface_01():
    '''Notes as contents.'''

    t = measuretools.AnonymousMeasure("c'8 d'8 e'8 f'8")

    r'''
    {
        \override Staff.TimeSignature #'stencil = ##f
        \time 1/2
        c'8
        d'8
        e'8
        f'8
        \revert Staff.TimeSignature #'stencil
    }
    '''

    assert t.contents_duration == Duration(4, 8)
    assert t.preprolated_duration == Duration(4, 8)
    assert t.prolated_duration == Duration(4, 8)
    assert t.prolation == 1

    assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/2\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.TimeSignature #'stencil\n}"


def test_AnonymousMeasure_duration_interface_02():
    '''Works with binary tuplet as contents.'''

    t = measuretools.AnonymousMeasure([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])

    r'''
    {
        \override Staff.TimeSignature #'stencil = ##f
        \time 1/4
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \revert Staff.TimeSignature #'stencil
    }
    '''

    assert t.contents_duration == Duration(2, 8)
    assert t.preprolated_duration == Duration(2, 8)
    assert t.prolated_duration == Duration(2, 8)
    assert t.prolation == 1

    assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/4\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t\\revert Staff.TimeSignature #'stencil\n}"


def test_AnonymousMeasure_duration_interface_03():
    '''Works with nonbinary tuplet.'''

    t = measuretools.AnonymousMeasure([Tuplet(Fraction(2, 3), "c'8 d'8 e'8 f'8")])
    t.denominator = 12

    r'''
    {
        \override Staff.TimeSignature #'stencil = ##f
        \time 4/12
        \times 2/3 {
            c'8
            d'8
            e'8
            f'8
        }
        \revert Staff.TimeSignature #'stencil
    }
    '''

    assert t.contents_duration == Duration(4, 12)
    assert t.preprolated_duration == Duration(4, 12)
    assert t.prolated_duration == Duration(4, 12)
    assert t.prolation == 1

    assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 4/12\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t\\revert Staff.TimeSignature #'stencil\n}"
