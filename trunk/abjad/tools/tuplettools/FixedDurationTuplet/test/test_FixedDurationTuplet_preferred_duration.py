from abjad import *


def test_FixedDurationTuplet_preferred_duration_01():

    t = tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 d'8 e'8 f'8 g'8 a'8")
    t.preferred_denominator = 4

    r'''
    \times 4/6 {
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\times 4/6 {\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n}"
