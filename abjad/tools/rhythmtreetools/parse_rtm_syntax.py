# -*- coding: utf-8 -*-
from abjad.tools import scoretools


def parse_rtm_syntax(rtm):
    r'''Parses RTM syntax.

    ..  container:: example

        **Example 1.** Parses tuplet:

        ::

            >>> rtm = '(1 (1 (1 (1 1)) 1))'
            >>> tuplet = rhythmtreetools.parse_rtm_syntax(rtm)
            >>> tuplet
            FixedDurationTuplet(Duration(1, 4), "c'8 c'16 c'16 c'8")

        ::

            >>> show(tuplet) # doctest: +SKIP

        ..  doctest::

            >>> print(format(tuplet))
            \times 2/3 {
                c'8
                c'16
                c'16
                c'8
            }

    ..  container:: example

        **Example 2.** Also supports fractional durations:

        ::

            >>> rtm = '(3/4 (1 1/2 (4/3 (1 -1/2 1))))'
            >>> tuplet = rhythmtreetools.parse_rtm_syntax(rtm)
            >>> tuplet
            FixedDurationTuplet(Duration(3, 16), "c'8 c'16 { 8/15 c'8 r16 c'8 }")

        ::

            >>> show(tuplet) # doctest: +SKIP

        ..  doctest::

            >>> print(format(_))
            \tweak text #tuplet-number::calc-fraction-text
            \times 9/17 {
                c'8
                c'16
                \tweak edge-height #'(0.7 . 0)
                \times 8/15 {
                    c'8
                    r16
                    c'8
                }
            }

    Returns fixed-duration tuplet or container.
    '''
    from abjad.tools import rhythmtreetools

    result = rhythmtreetools.RhythmTreeParser()(rtm)

    con = scoretools.Container()

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
