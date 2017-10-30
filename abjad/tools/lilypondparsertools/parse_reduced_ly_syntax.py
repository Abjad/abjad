from abjad.tools.lilypondparsertools.ReducedLyParser import ReducedLyParser


def parse_reduced_ly_syntax(string):
    r'''Parse the reduced LilyPond rhythmic syntax:

    >>> from abjad.tools import lilypondparsertools

    ..  container:: example

        >>> string = '4 -4. 8.. 5/3 { } 4'
        >>> container = lilypondparsertools.parse_reduced_ly_syntax(string)

        >>> for component in container:
        ...     component
        ...
        Note("c'4")
        Rest('r4.')
        Note("c'8..")
        Tuplet(Multiplier(5, 3), '')
        Note("c'4")

    Returns list.
    '''
    return ReducedLyParser()(string)
