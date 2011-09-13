from abjad import *


def test_DynamicMeasure_duration_interface_01():
    '''Notes as contents.'''

    t = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")
    t.denominator = 8

    r'''
    {
        \time 4/8
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.contents_duration == Duration(4, 8)
    assert t.preprolated_duration == Duration(4, 8)
    assert t.prolated_duration == Duration(4, 8)
    assert t.prolation == 1

    assert t.format == "{\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_DynamicMeasure_duration_interface_02():
    '''Binary tuplet as contents.'''

    t = measuretools.DynamicMeasure([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
    t.denominator = 8

    r'''
    {
        \time 2/8
        \times 2/3 {
            c'8
            d'8
            e'8
        }
    }
    '''

    assert t.contents_duration == Duration(2, 8)
    assert t.preprolated_duration == Duration(2, 8)
    assert t.prolated_duration == Duration(2, 8)
    assert t.prolation == 1

    assert t.format == "{\n\t\\time 2/8\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n}"


def test_DynamicMeasure_duration_interface_03():
    '''Nonbinary tuplet as contents.'''

    t = measuretools.DynamicMeasure([Tuplet(Fraction(2, 3), "c'8 d'8 e'8 f'8")])
    t.denominator = 12

    r'''
    {
        \time 4/12
        \times 2/3 {
            c'8
            d'8
            e'8
            f'8
        }
    }
    '''

    assert t.contents_duration == Duration(4, 12)
    assert t.preprolated_duration == Duration(4, 12)
    assert t.prolated_duration == Duration(4, 12)
    assert t.prolation == 1

    assert t.format == "{\n\t\\time 4/12\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"
