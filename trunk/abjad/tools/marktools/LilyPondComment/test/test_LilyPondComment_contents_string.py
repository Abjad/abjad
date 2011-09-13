from abjad import *


def test_LilyPondComment_contents_string_01():
    '''LilyPondComment contents string is read / write.
    '''

    comment = marktools.LilyPondComment('contents string')
    assert comment.contents_string == 'contents string'

    comment.contents_string = 'new contents string'
    assert comment.contents_string == 'new contents string'
