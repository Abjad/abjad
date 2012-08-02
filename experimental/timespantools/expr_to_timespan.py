def expr_to_timespan(expr):
    r'''.. versionadded:: 1.0

    Return `expr` unchanged when `expr` is timespan.

    Return ``expr.timespan`` when `expr` has timespan.

    Otherwise raise exception.
    '''
    from experimental import timespantools

    if isinstance(expr, timespantools.Timespan):
        return expr
    else:
        return expr.timespan
