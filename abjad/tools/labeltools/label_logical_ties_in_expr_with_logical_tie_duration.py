# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_logical_ties_in_expr_with_logical_tie_duration(
    expr, direction=Down):
    r'''Label logical ties in `expr` with logical tie durations:

    ::

        >>> staff = Staff(r"\times 2/3 { c'8 ~ c'8 c'8 ~ } c'8")
        >>> labeltools.label_logical_ties_in_expr_with_logical_tie_duration(staff)

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \times 2/3 {
                c'8 ~ _ \markup { \small 1/6 }
                c'8
                c'8 ~ _ \markup { \small 5/24 }
            }
            c'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''
    logical_ties = iterate(expr).by_logical_tie()
    for index, logical_tie in enumerate(logical_ties):
        duration = logical_tie.get_duration()
        label = markuptools.Markup(duration, direction=direction)
        label = label.small()
        attach(label, logical_tie.head)