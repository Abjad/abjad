from abjad.tools import durationtools


def multiply_and_scale_contents_of_measures_in_expr(expr, multiplier_pairs):
    '''.. versionadded:: 1.1

    Multiply and scale contents of measures in `expr` by `multiplier_pairs`.

    The `multiplier_pairs` argument must be a list of 
    ``(contents_multiplier, denominator_multiplier)`` pairs.

    Both `contents_multiplier` and `denominator_multiplier` must be positive integers.

    Example 1. Multiply measure contents by ``3``. Scale time signature denominator by ``3``::

        >>> measure = Measure((3, 16), "c'16 c'16 c'16")

    ::

        >>> measuretools.multiply_and_scale_contents_of_measures_in_expr(measure, [(3, 3)])
        [Measure(9/48, [c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32])]

    Example 2. Multiply measure contents by ``3``. Scale time signature denominator by ``2``::

        >>> measure = Measure((3, 16), "c'16 c'16 c'16")

    ::

        >>> measuretools.multiply_and_scale_contents_of_measures_in_expr(measure, [(3, 2)])
        [Measure(9/32, [c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32])]

    Example 3. Multiply measure contents ``3``::

        >>> measure = Measure((3, 16), "c'16 c'16 c'16")

    ::

        >>> measuretools.multiply_and_scale_contents_of_measures_in_expr(measure, [(3, 1)])
        [Measure(9/16, [c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16])]

    Return list of measures changed.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import measuretools

    assert isinstance(multiplier_pairs, list)
    assert all([isinstance(pair, tuple) for pair in multiplier_pairs])

    result = []
    num_pairs = len(multiplier_pairs)
    for i, measure in enumerate(iterationtools.iterate_measures_in_expr(expr)):
        concentration_pair = multiplier_pairs[i % num_pairs]
        assert isinstance(concentration_pair, tuple)
        spin_count, scalar_denominator = concentration_pair
        measuretools.multiply_contents_of_measures_in_expr(measure, spin_count)
        multiplier = durationtools.Duration(1, scalar_denominator)
        measuretools.scale_measure_and_adjust_time_signature(measure, multiplier)
        result.append(measure)

    return result
