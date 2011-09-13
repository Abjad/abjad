from abjad import *


def test_measuretools_scale_contents_of_measures_in_expr_01():
    '''Quadruple binary meter.
    Time siganture denominator adjust appropriately.'''

    t = Measure((3, 32), "c'32 d'32 e'32")
    spannertools.BeamSpanner(t[:])

    measuretools.scale_contents_of_measures_in_expr(t, Duration(4))

    r'''
    {
        \time 3/8
        c'8 [
        d'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/8\n\tc'8 [\n\td'8\n\te'8 ]\n}"


def test_measuretools_scale_contents_of_measures_in_expr_02():
    '''Triple binary meter.'''

    t = Measure((3, 32), "c'32 d'32 e'32")
    spannertools.BeamSpanner(t[:])

    measuretools.scale_contents_of_measures_in_expr(t, Duration(3))

    r'''
    {
        \time 9/32
        c'16. [
        d'16.
        e'16. ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 9/32\n\tc'16. [\n\td'16.\n\te'16. ]\n}"


def test_measuretools_scale_contents_of_measures_in_expr_03():
    '''Multiply binary measure by 2/3.'''

    t = Measure((3, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])

    measuretools.scale_contents_of_measures_in_expr(t, Duration(2, 3))

    r'''
    {
        \time 3/12
        \scaleDurations #'(2 . 3) {
            c'8 [
            d'8
            e'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8 [\n\t\td'8\n\t\te'8 ]\n\t}\n}"
