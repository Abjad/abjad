from abjad import *
import py.test


def test_LilyPondComment___setattr___01():
    '''Slots constrain comment attributes.
    '''

    comment = marktools.LilyPondComment('foo')

    assert py.test.raises(AttributeError, "comment.foo = 'bar'")
