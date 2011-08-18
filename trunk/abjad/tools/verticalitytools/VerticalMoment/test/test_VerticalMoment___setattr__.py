from abjad import *
from abjad.tools import verticalitytools
import py.test


def test_VerticalMoment___setattr___01():
    '''Vertical moments are immutable.
    '''

    vertical_moment = verticalitytools.get_vertical_moment_starting_with_component(Note('c4'))
    assert py.test.raises(AttributeError, "vertical_moment.foo = 'bar'")
