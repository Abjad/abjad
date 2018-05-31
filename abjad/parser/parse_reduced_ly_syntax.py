from .ReducedLyParser import ReducedLyParser


def parse_reduced_ly_syntax(string):
    """
    Parse the reduced LilyPond rhythmic syntax:

    ..  container:: example

        >>> string = '4 -4. 8.. 5/3 { } 4'
        >>> container = abjad.parser.parse_reduced_ly_syntax(string)

        >>> for component in container:
        ...     component
        ...
        Note("c'4")
        Rest('r4.')
        Note("c'8..")
        Tuplet(Multiplier(5, 3), '')
        Note("c'4")

    Returns list.
    """
    return ReducedLyParser()(string)
