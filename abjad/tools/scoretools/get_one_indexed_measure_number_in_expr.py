# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import select


def get_one_indexed_measure_number_in_expr(expr, measure_number):
    r'''Gets one-indexed `measure_number` in `expr`.

    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }

    ::

        >>> scoretools.get_one_indexed_measure_number_in_expr(staff, 3)
        Measure(2/8, [g'8, a'8])

    Note that measures number from ``1``.
    '''
    from abjad.tools import scoretools

    # check input
    if measure_number < 1:
        message = 'measure numbers allow only positive integers.'
        raise ValueError(message)

    # calculate measure index
    measure_index = measure_number - 1

    # return measure
    selection = select(expr)
    return selection._get_component(scoretools.Measure, measure_index)
