from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr
from abjad.tools.measuretools.multiply_contents_of_measures_in_expr import multiply_contents_of_measures_in_expr
from abjad.tools.measuretools.scale_measure_by_multiplier_and_adjust_meter import scale_measure_by_multiplier_and_adjust_meter
from abjad.tools import durationtools


def multiply_contents_of_measures_in_expr_and_scale_meter_denominators(expr, concentration_pairs):
    '''.. versionadded:: 1.1

    Mutiply contents of measures in `expr` and scale meter denominators.

    Expr may be any Abjad expression.
    Concentration_pairs a Python list of pairs,
    each of the form (spin_count, scalar_denominator).
    Both spin_count and scalar_denominator must be positive integers.

    Iterate expr. For every measure in expr,
    spin measure by the spin_count element in concentration_pair and
    scale measure by 1/scalar_denominator element in concentration_pair.

    Return Python list of transformed measures::

        abjad> t = Measure((3, 16), notetools.make_repeated_notes(3, Duration(1, 16)))
        abjad> print(measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators(t, [(3, 3)])[0])
        |9/48, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32|

    ::

        abjad> t = Measure((3, 16), notetools.make_repeated_notes(3, Duration(1, 16)))
        abjad> print(measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators(t, [(3, 2)])[0])
        |9/32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32|

    ::

        abjad> t = Measure((3, 16), notetools.make_repeated_notes(3, Duration(1, 16)))
        abjad> print(measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators(t, [(3, 1)])[0])
        |9/16, c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16|

    .. versionchanged:: 2.0
        renamed ``measuretools.concentrate()`` to
        ``measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators()``.
    '''

    assert isinstance(concentration_pairs, list)
    assert all([isinstance(pair, tuple) for pair in concentration_pairs])

    result = []
    num_pairs = len(concentration_pairs)
    for i, measure in enumerate(iterate_measures_forward_in_expr(expr)):
        concentration_pair = concentration_pairs[i % num_pairs]
        assert isinstance(concentration_pair, tuple)
        spin_count, scalar_denominator = concentration_pair
        multiply_contents_of_measures_in_expr(measure, spin_count)
        multiplier = durationtools.Duration(1, scalar_denominator)
        scale_measure_by_multiplier_and_adjust_meter(measure, multiplier)
        result.append(measure)

    return result
