from abjad.tools.rhythmtreetools._RTMParser import _RTMParser


def parse_rtm_syntax(rtm):
    '''Parse RTM syntax:

    ::

        abjad> from abjad.tools.rhythmtreetools import parse_rtm_syntax

    ::

        abjad> rtm = '(1 (1 (1 (1 1)) 1))'
        abjad> result = parse_rtm_syntax(rtm)
        abjad> result
        FixedDurationTuplet(1/4, [c'8, {@ 1:1 c'16, c'16 @}, c'8])

    Returns `FixedDurationTuplet` instance.
    '''

    return _RTMParser()(rtm)()
