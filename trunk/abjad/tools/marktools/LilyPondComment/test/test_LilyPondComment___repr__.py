from abjad import *
from abjad.tools.marktools import LilyPondComment


def test_LilyPondComment___repr___01():
    '''Repr of unattached comment is evaluable.
    '''

    comment_1 = marktools.LilyPondComment('foo')
    comment_2 = eval(repr(comment_1))

    assert isinstance(comment_1, marktools.LilyPondComment)
    assert isinstance(comment_2, marktools.LilyPondComment)
    assert comment_1 == comment_2
