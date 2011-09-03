from abjad import *
import py.test


def test_Voice___setattr___01():
    '''Slots constrain voice attributes.
    '''

    voice = Voice([])

    assert py.test.raises(AttributeError, "voice.foo = 'bar'")
