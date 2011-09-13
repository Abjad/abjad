from abjad import *
import py.test


def test_Measure_duration_01():
    '''Binary meter, properly filled.'''

    t = Measure((3, 8), "c'8 d'8 e'8")

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert t.contents_duration == Duration(3, 8)
    assert t.preprolated_duration == Duration(3, 8)
    assert t.prolated_duration == Duration(3, 8)
    assert t.prolation == 1

    assert t.format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"


def test_Measure_duration_02():
    '''Nonbinary meter, properly filled.'''

    t = Measure((3, 10), "c'8 d'8 e'8")

    r'''
    {
        \time 3/10
        \scaleDurations #'(4 . 5) {
            c'8
            d'8
            e'8
        }
    }
    '''

    assert t.contents_duration == Duration(3, 8)
    assert t.preprolated_duration == Duration(3, 10)
    assert t.prolated_duration == Duration(3, 10)
    assert t.prolation == 1

    assert t.format == "{\n\t\\time 3/10\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n}"



def test_Measure_duration_03():
    '''Binary meter, improperly filled.'''

    t = Measure((3, 8), "c'8 d'8 e'8 f'8")

    assert py.test.raises(OverfullMeasureError, 't.format')

    assert t.contents_duration == Duration(4, 8)
    assert t.preprolated_duration == Duration(4, 8)
    assert t.prolated_duration == Duration(4, 8)
    assert t.prolation == 1


def test_Measure_duration_04():
    '''Nonbinary meter, improperly filled.'''

    t = Measure((3, 10), "c'8 d'8 e'8 f'8")

    assert py.test.raises(OverfullMeasureError, 't.format')

    assert t.contents_duration == Duration(4, 8)
    assert t.preprolated_duration == Duration(4, 10)
    assert t.prolated_duration == Duration(4, 10)
    assert t.prolation == 1
