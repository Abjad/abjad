from abjad import *
import py.test


def test_Measure_duration_01():
    '''Properly filled Measure with power-of-two time signature denominator.
    '''

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
    assert t.duration == Duration(3, 8)
    assert t.prolation == 1

    assert t.lilypond_format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"


def test_Measure_duration_02():
    '''Properly filled measure without power-of-two time signature denominator.
    '''

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
    assert t.duration == Duration(3, 10)
    assert t.prolation == 1

    assert t.lilypond_format == "{\n\t\\time 3/10\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n}"



def test_Measure_duration_03():
    '''Improperly filled measure without power-of-two time signature denominator.
    '''

    t = Measure((3, 8), "c'8 d'8 e'8 f'8")

    assert py.test.raises(OverfullContainerError, 't.lilypond_format')

    assert t.contents_duration == Duration(4, 8)
    assert t.preprolated_duration == Duration(4, 8)
    assert t.duration == Duration(4, 8)
    assert t.prolation == 1


def test_Measure_duration_04():
    '''Impropely filled measure without power-of-two time signature denominator.
    '''

    t = Measure((3, 10), "c'8 d'8 e'8 f'8")

    assert py.test.raises(OverfullContainerError, 't.lilypond_format')

    assert t.contents_duration == Duration(4, 8)
    assert t.preprolated_duration == Duration(4, 10)
    assert t.duration == Duration(4, 10)
    assert t.prolation == 1
