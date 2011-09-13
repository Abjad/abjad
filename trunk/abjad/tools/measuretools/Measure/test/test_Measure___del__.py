from abjad import *


def test_Measure___del___01():
    '''Nonnegative indices work.'''

    t = Measure((4, 8), Note(0, (1, 8)) * 4)
    del(t[:1])

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_Measure___del___02():
    '''Negative indices work.'''

    t = Measure((4, 8), Note(0, (1, 8)) * 4)
    del(t[-1:])

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_Measure___del___03():
    '''Denominator preservation in meter.'''

    t = Measure((4, 8), Note(0, (1, 8)) * 4)
    del(t[:2])

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 2/8\n\tc'8\n\tc'8\n}"


def test_Measure___del___04():
    '''Denominator changes from 8 to 16.'''

    t = Measure((4, 8), Note(0, (1, 16)) * 2 + Note(0, (1, 8)) * 3)
    del(t[:1])

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 7/16\n\tc'16\n\tc'8\n\tc'8\n\tc'8\n}"


def test_Measure___del___05():
    '''Trim nonbinary measure.'''

    t = Measure((4, 9), "c'8 d'8 e'8 f'8")
    del(t[:1])

    r'''
    {
        \time 3/9
        \scaleDurations #'(8 . 9) {
            d'8
            e'8
            f'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/9\n\t\\scaleDurations #'(8 . 9) {\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"
    #assert t.format == "{\n\t\\scaleDurations #'(8 . 9) {\n\t\t\\time 3/9\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"


def tet_rigid_measure_trim_06():
    '''Trim nonbinary measure, with denominator change.'''

    notes = "c'8 d'8 e'8 f'8"
    notes[0].written_duration = Duration(1, 16)
    notes[1].written_duration = Duration(1, 16)
    t = Measure((3, 9), notes)

    r'''
    {
        \time 3/9
        \scaleDurations #'(8 . 9) {
            c'16
            d'16
            e'8
            f'8
        }
    }
    '''

    del(t[:1])

    r'''
    {
        \time 5/18
        \scaleDurations #'(8 . 9) {
            d'16
            e'8
            f'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\td'16\n\t\te'8\n\t\tf'8\n\t}\n}"
