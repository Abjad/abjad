from abjad.tools import containertools


def parse_rtm_syntax(rtm):
    r'''Parse RTM syntax:

    ::

        >>> rtm = '(1 (1 (1 (1 1)) 1))'
        >>> rhythmtreetools.parse_rtm_syntax(rtm)
        FixedDurationTuplet(1/4, [c'8, c'16, c'16, c'8])

    Also supports fractional durations:

    ::

        >>> rtm = '(3/4 (1 1/2 (4/3 (1 -1/2 1))))'
        >>> rhythmtreetools.parse_rtm_syntax(rtm)
        FixedDurationTuplet(3/16, [c'8, c'16, {@ 15:8 c'8, r16, c'8 @}])
        >>> f(_)
        \fraction \times 9/17 {
            c'8
            c'16
            \times 8/15 {
                c'8
                r16
                c'8
            }
        }

    Return `FixedDurationTuplet` or `Container` instance.
    '''
    from abjad.tools import rhythmtreetools

    result = rhythmtreetools.RhythmTreeParser()(rtm)

    con = containertools.Container()

    for node in result:
        tuplet = node((1, 4))
        # following line added 2012-08-01. tb.
        tuplet = tuplet[0]
        if tuplet.is_trivial:
            con.extend(tuplet[:])
        else:
            con.append(tuplet)

    if len(con) == 1:
        return con[0]
    return con
