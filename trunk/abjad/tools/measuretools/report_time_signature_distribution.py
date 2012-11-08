import itertools


def report_time_signature_distribution(expr):
    r'''.. versionadded:: 2.0

    Report time signature distribution of `expr`::

        >>> staff = Staff(r"abj: | 2/4 c'4 d'4 || 2/4 e'4 f'4 || 2/4 g'2 || 5/8 c'8 d'8 e'8 f'8 g'8 |")

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/4
                c'4
                d'4
            }
            {
                e'4
                f'4
            }
            {
                g'2
            }
            {
                \time 5/8
                c'8
                d'8
                e'8
                f'8
                g'8
            }
        }

    ::

        >>> print measuretools.report_time_signature_distribution(staff)
            2/4 3
            5/8 1

    Return string.
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

    return result
