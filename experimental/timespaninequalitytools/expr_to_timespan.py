import numbers
from abjad.tools import sequencetools


def expr_to_timespan(expr):
    r'''.. versionadded:: 1.0

    Return `expr` unchanged when `expr` is timespan.

    Return ``expr.timespan`` when `expr` has timespan.

    Return timespan constant when `expr` is a number::

        >>> timespaninequalitytools.expr_to_timespan(Fraction(7, 8))
        TimespanConstant(start_offset=Offset(7, 8), stop_offset=Offset(7, 8))

    Return timespan constant when `expr` is an offset::

        >>> timespaninequalitytools.expr_to_timespan(durationtools.Offset(7, 8))
        TimespanConstant(start_offset=Offset(7, 8), stop_offset=Offset(7, 8))

    Return timespan constant when `expr` is a pair::

        >>> timespaninequalitytools.expr_to_timespan(((1, 2), (3, 2)))
        TimespanConstant(start_offset=Offset(1, 2), stop_offset=Offset(3, 2))

    Otherwise raise type error.
    '''
    from experimental import timespaninequalitytools

    if isinstance(expr, timespaninequalitytools.Timespan):
        return expr
    if hasattr(expr, 'timespan'):
        return expr.timespan
    elif isinstance(expr, numbers.Number):
        return timespantools.TimespanConstant(start_offset=expr, stop_offset=expr)
    elif sequencetools.is_pair(expr):
        start_offset, stop_offset = expr
        return timespantools.TimespanConstant(start_offset=start_offset, stop_offset=stop_offset)
    else:
        raise TypeError('can not change {!r} to timespan.'.format(expr))
