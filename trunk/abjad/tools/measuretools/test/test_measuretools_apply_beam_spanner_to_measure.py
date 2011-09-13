from abjad import *


def test_measuretools_apply_beam_spanner_to_measure_01():

    measure = Measure((2, 8), notetools.make_repeated_notes(2))

    r'''
    {
        \time 2/8
        c'8
        c'8
    }
    '''

    measuretools.apply_beam_spanner_to_measure(measure)


    r'''
    {
        \time 2/8
        c'8 [
        c'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(measure)
    assert measure.format == "{\n\t\\time 2/8\n\tc'8 [\n\tc'8 ]\n}"
