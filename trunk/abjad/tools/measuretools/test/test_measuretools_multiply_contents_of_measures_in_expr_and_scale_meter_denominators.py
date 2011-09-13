from abjad import *


def test_measuretools_multiply_contents_of_measures_in_expr_and_scale_meter_denominators_01():
    '''Concentrate one measure three times.
        Time signature 3/8 goes to 9/24.
        Numerator and denominator both triple.'''

    t = Measure((3, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators(t, [(3, 3)])

    r'''
    {
        \time 9/24
        \scaleDurations #'(2 . 3) {
            c'16 [
            d'16
            e'16 ]
            c'16 [
            d'16
            e'16 ]
            c'16 [
            d'16
            e'16 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 9/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t}\n}"


def test_measuretools_multiply_contents_of_measures_in_expr_and_scale_meter_denominators_02():
    '''Concentrate one measure four times over five.
    Time signature 3/16 goes to 12/80.
    Numerator quadruples and denominator quintuples.
    '''

    t = Measure((3, 16), "c'16 d'16 e'16")
    spannertools.BeamSpanner(t[:])
    measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators(t, [(4, 5)])

    r'''
    {
        \time 12/80
        \scaleDurations #'(4 . 5) {
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 12/80\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t}\n}"


def test_measuretools_multiply_contents_of_measures_in_expr_and_scale_meter_denominators_03():
    '''Concentrate one measure four times over four.
        Time signature 3/16 goes to 12/64.
        Numerator and denominator both quadruple.'''

    t = Measure((3, 16), "c'16 d'16 e'16")
    spannertools.BeamSpanner(t[:])
    measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators(t, [(4, 4)])

    r'''
    {
        \time 12/64
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 12/64\n\tc'64 [\n\td'64\n\te'64 ]\n\tc'64 [\n\td'64\n\te'64 ]\n\tc'64 [\n\td'64\n\te'64 ]\n\tc'64 [\n\td'64\n\te'64 ]\n}"


def test_measuretools_multiply_contents_of_measures_in_expr_and_scale_meter_denominators_04():
    '''Concentrate one measure two times over four.
        Time signature 3/16 goes to 6/64.
        Numerator doubles and denominator quadruples.'''

    t = Measure((3, 16), "c'16 d'16 e'16")
    spannertools.BeamSpanner(t[:])
    measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators(t, [(2, 4)])

    r'''
    {
        \time 6/64
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 6/64\n\tc'64 [\n\td'64\n\te'64 ]\n\tc'64 [\n\td'64\n\te'64 ]\n}"
