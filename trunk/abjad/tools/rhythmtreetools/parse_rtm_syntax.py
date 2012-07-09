from abjad.tools import containertools
from abjad.tools.rhythmtreetools.RhythmTreeParser import RhythmTreeParser


def parse_rtm_syntax(rtm):
    '''Parse RTM syntax:

    ::

        >>> from abjad.tools.rhythmtreetools import parse_rtm_syntax

    ::

        >>> rtm = '(1 (1 (1 (1 1)) 1))'
        >>> result = parse_rtm_syntax(rtm)
        >>> result
        FixedDurationTuplet(1/4, [c'8, c'16, c'16, c'8])

    Return `FixedDurationTuplet` or `Container` instance.
    '''

    result = RhythmTreeParser()(rtm)

    con = containertools.Container()

    for node in result:
        tuplet = node((1, 4))
        if tuplet.is_trivial:
            con.extend(tuplet[:])
        else:
            con.append(tuplet)

    if len(con) == 1:
        return con[0]
    return con
