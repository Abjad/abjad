from abjad import Container
from abjad.tools.rhythmtreetools._RTMParser import _RTMParser


def parse_rtm_syntax(rtm):
    '''Parse RTM syntax:

    ::

        abjad> from abjad.tools.rhythmtreetools import parse_rtm_syntax

    ::

        abjad> rtm = '(1 (1 (1 (1 1)) 1))'
        abjad> result = parse_rtm_syntax(rtm)
        abjad> result
        FixedDurationTuplet(1/4, [c'8, c'16, c'16, c'8])

    Returns `FixedDurationTuplet` or `Container` instance.
    '''

    result = _RTMParser()(rtm)

    if 1 < len(result):
        con = Container()
        for node in result:
            tuplet = node()
            if tuplet.is_trivial:
                con.extend(tuplet[:])
            else:
                con.append(tuplet)
        return con

    else:
        tuplet = result[0]()
        if tuplet.is_trivial:
            con = Container()
            con.extend(tuplet[:])
            return con
        return tuplet
