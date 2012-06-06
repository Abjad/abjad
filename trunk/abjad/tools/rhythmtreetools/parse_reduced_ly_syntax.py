from abjad.tools.rhythmtreetools._TupletParser import _TupletParser


def parse_reduced_ly_syntax(string):
    '''Parse the reduced LilyPond rhythmic syntax:

    ::

        >>> from abjad.tools.rhythmtreetools import parse_reduced_ly_syntax

    ::

        >>> string = '4 -4. 8.. 5/3 { 2/3 {(3, 8)} (3, 8) -8 } 4'
        >>> result = parse_reduced_ly_syntax(string)
        >>> for x in result:
        ...     x
        ...
        Note("c'4")
        Rest('r4.')
        Note("c'8..")
        Tuplet(5/3, [{* 3:2 FixedDurationContainer(Duration(3, 8), []) *}, FixedDurationContainer(Duration(3, 8), []), r8])
        Note("c'4")

    Return list.
    '''

    return _TupletParser()(string)
