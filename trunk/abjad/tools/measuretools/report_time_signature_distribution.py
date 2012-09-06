def report_time_signature_distribution(expr):
    r'''.. versionadded:: 2.0

    Report meter distribution of `expr` as string::

        >>> measuretools.report_time_signature_distribution(t) # doctest: +SKIP
        '\t3/80\t2\n\t2/16\t73\n\t7/40\t1\n\t3/16\t20\n\t16/80\t1\n\t17/80\t1\n
        \t19/80\t1\n\t4/16\t73\n\t5/16\t62\n\t13/40\t1\n\t27/80\t1\n\t6/16\t12\
        n\t7/16\t16\n\t8/16\t13\n\t9/16\t15\n\t10/16\t4\n'

    Return string.
    '''
    from abjad.tools.measuretools._report_meter_distribution import _report_meter_distribution

    return _report_meter_distribution(expr, delivery='string')
