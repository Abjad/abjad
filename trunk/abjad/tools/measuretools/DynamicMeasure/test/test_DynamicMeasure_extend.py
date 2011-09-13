from abjad import *


def test_DynamicMeasure_extend_01():
    '''Dynamic measures adjust their signatures after being extended.
    '''

    measure = measuretools.DynamicMeasure("c'8 d'8 e'8")
    measure.extend([Note("fs'8"), Note("gs'8")])

    r'''
    {
        \time 5/8
        c'8
        d'8
        e'8
        fs'8
        gs'8
    }
    '''

    assert measure.format == "{\n\t\\time 5/8\n\tc'8\n\td'8\n\te'8\n\tfs'8\n\tgs'8\n}"
