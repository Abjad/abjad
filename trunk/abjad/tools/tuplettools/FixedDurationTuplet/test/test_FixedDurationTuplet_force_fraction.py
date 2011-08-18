from abjad import *


def test_FixedDurationTuplet_force_fraction_01():

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t.force_fraction = True

    r'''
    \fraction \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert t.format == "\\fraction \\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}"
