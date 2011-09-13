from abjad import *
import py.test


def test_DynamicMeasure_meter_assignment_01():
    '''Dynamic measures block meter assignment.
    '''

    measure = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")

    r'''
    {
        \time 1/2
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert py.test.raises(ExtraMarkError, 'contexttools.TimeSignatureMark((4, 8))(measure)')
