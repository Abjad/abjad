from abjad import *
from abjad.tools import verticalitytools


def test_VerticalMoment___repr___01():
    '''Vertical moment repr returns a nonempty string.
    '''

    vertical_moment = Note('c4').select_vertical_moment()
    representation = repr(vertical_moment)

    assert isinstance(representation, str) and 0 < len(representation)
