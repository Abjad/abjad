import itertools


# TODO: make public
# TODO: remove string-valued delivery='screen' keyword altogether
def _report_time_signature_distribution(expr, delivery='screen'):
    r'''Inventory time signatures in `expr` with frequency count of each.

    When ``delivery='screen'`` print results to stdout::

        >>> from abjad.tools.measuretools._report_time_signature_distribution import _report_time_signature_distribution
        >>> _report_time_signature_distribution(t) # doctest: +SKIP
            2/16    62
            3/16    14
            4/16    66
            5/16    57
            6/16    17
            7/16    20
            8/16    16
            9/16    19
            10/16   4

    When ``delivery='string'`` return results as a single string. ::

        >>> measuretools.report_time_signature_distribution(t, delivery='string') # doctest: +SKIP
        '\t3/80\t2\n\t2/16\t73\n\t7/40\t1\n\t3/16\t20\n\t16/80\t1\n\t17/80\t1\n
        \t19/80\t1\n\t4/16\t73\n\t5/16\t62\n\t13/40\t1\n\t27/80\t1\n\t6/16\t12\
        n\t7/16\t16\n\t8/16\t13\n\t9/16\t15\n\t10/16\t4\n'

    Return string or none.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools

    time_signatures = []
    for measure in iterationtools.iterate_measures_in_expr(expr):
        time_signatures.append(contexttools.get_effective_time_signature(measure))

    time_signatures.sort()

    result = ''
    for key, values_generator in itertools.groupby(time_signatures):
        result += '\t%s\t%s\n' % (key, len(list(values_generator)))

    if delivery == 'screen':
        print result
    elif delivery == 'string':
        return result
    else:
        raise ValueError("delivery must be 'screen' or 'string'.")
