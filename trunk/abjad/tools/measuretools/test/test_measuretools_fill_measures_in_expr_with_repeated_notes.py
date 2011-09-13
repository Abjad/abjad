from abjad import *


def test_measuretools_fill_measures_in_expr_with_repeated_notes_01():
    '''Populate nonbinary measure with note train.'''

    t = Measure((5, 18), [])
    measuretools.fill_measures_in_expr_with_repeated_notes(t, Duration(1, 16))

    r'''
    {
        \time 5/18
        \scaleDurations #'(8 . 9) {
            c'16
            c'16
            c'16
            c'16
            c'16
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n}"
