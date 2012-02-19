from abjad import *
from abjad.tools.instrumenttools import *
from abjad.tools.scoretools import Performer


def test_Performer___hash___01():
    '''If two Performers compare equally, their hashes also compare equally.'''
    one = Performer(name='Guitar', instruments=[Guitar( )])
    two = Performer(name='Guitar', instruments=[Guitar( )])
    three = Performer(name='Flute', instruments=[AltoFlute( )])
    assert one == two
    assert hash(one) == hash(two)
    assert one != three
    assert hash(one) != hash(three)
