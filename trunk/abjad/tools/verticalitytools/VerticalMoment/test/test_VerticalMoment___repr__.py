from abjad import *
from abjad.tools import verticalitytools


def test_VerticalMoment___repr___01():
    '''Vertical moment repr returns a nonempty string.
    '''

    vertical_moment = verticalitytools.get_vertical_moment_starting_with_component(Note('c4'))
    representation = repr(vertical_moment)

    assert isinstance(representation, str) and 0 < len(representation)
