def measure_to_one_line_input_string(measure):
    r'''.. versionadded:: 2.6

    Change `measure` to one-line input string::

        >>> measure = Measure((4, 4), "c'4 d'4 e'4 f'4")

    ::

        >>> input_string = measuretools.measure_to_one_line_input_string(measure)

    ::

        >>> print input_string
        Measure((4, 4), "c'4 d'4 e'4 f'4")

    ::

        >>> new_measure = eval(input_string)

    ::

        >>> new_measure
        Measure(4/4, [c'4, d'4, e'4, f'4])

    ::

        >>> f(new_measure)
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }

    The purpose of this function is to create an evaluable string from simple measures.

    Spanners, articulations and overrides not supported.

    Return string.
    '''
    from abjad.tools import contexttools

    time_signature = contexttools.get_effective_time_signature(measure)
    pair = (time_signature.numerator, time_signature.denominator)
    contents_string = ' '.join([str(x) for x in measure])

    result = '%s(%s, %r)' % (type(measure).__name__, pair, contents_string)

    return result
