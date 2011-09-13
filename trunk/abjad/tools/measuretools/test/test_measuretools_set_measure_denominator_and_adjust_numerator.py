from abjad import *


def test_measuretools_set_measure_denominator_and_adjust_numerator_01():

    t = Measure((3, 8), "c'8 d'8 e'8")
    measuretools.set_measure_denominator_and_adjust_numerator(t, 16)

    r'''
    {
        \time 6/16
        c'8
        d'8
        e'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 6/16\n\tc'8\n\td'8\n\te'8\n}"

    measuretools.set_measure_denominator_and_adjust_numerator(t, 8)

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"
