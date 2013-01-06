import collections


def count_offsets_in_expr(expr):
    r'''Count offsets in `expr`.
    
    Example 1.:
    
    ::

        >>> score = Score()
        >>> score.append(Staff("c'4. d'8 e'2"))
        >>> score.append(Staff(r'\clef bass c4 b,4 a,2'))
        >>> f(score)
        \new Score <<
            \new Staff {
                c'4.
                d'8
                e'2
            }
            \new Staff {
                \clef "bass"
                c4
                b,4
                a,2
            }
        >>

    ::

        >>> durationtools.count_offsets_in_expr(score.leaves)
        Counter({Offset(1, 2): 4, Offset(0, 1): 2, Offset(3, 8): 2, Offset(1, 4): 2, Offset(1, 1): 2})

    Example 2.:

    ::

        >>> a = timespantools.Timespan(0, 10)
        >>> b = timespantools.Timespan(5, 15)
        >>> c = timespantools.Timespan(15, 20)

    ::

        >>> durationtools.count_offsets_in_expr((a, b, c))
        Counter({Offset(15, 1): 2, Offset(0, 1): 1, Offset(10, 1): 1, Offset(20, 1): 1, Offset(5, 1): 1})

    Return Counter.
    '''
    from abjad.tools import durationtools
    counter = collections.Counter()
    for x in expr:
        if hasattr(x, 'start_offset') and hasattr(x, 'stop_offset'):
            counter[x.start_offset] += 1
            counter[x.stop_offset] += 1
        elif hasattr(x, 'timespan'):
            counter[x.timespan.start_offset] += 1
            counter[x.timespan.stop_offset] += 1
        else:
            offset = durationtools.Offset(x)
            counter[offset] += 1
    return counter
