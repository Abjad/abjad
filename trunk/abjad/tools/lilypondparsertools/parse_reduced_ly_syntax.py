from abjad.tools.lilypondparsertools.ReducedLyParser import ReducedLyParser


def parse_reduced_ly_syntax(string):
    '''Parse the reduced LilyPond rhythmic syntax:

        >>> from abjad.tools import lilypondparsertools

    ::

        >>> string = '4 -4. 8.. 5/3 { } 4'
        >>> result = lilypondparsertools.parse_reduced_ly_syntax(string)

    ::

        >>> for x in result:
        ...     x
        ...
        Note("c'4")
        Rest('r4.')
        Note("c'8..")
        Tuplet(5/3, [])
        Note("c'4")

    Return list.
    '''

    return ReducedLyParser()(string)
