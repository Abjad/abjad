# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_LilyPondComment___init___01():
    r'''Initialize LilyPond comment from contents string.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner()
    attach(slur, staff.select_leaves())
    comment = marktools.LilyPondComment('beginning of note content')
    comment.attach(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            % beginning of note content
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_marktools_LilyPondComment___init___02():
    r'''Initialize LilyPond comment from contents string and format slot.
    '''

    comment = marktools.LilyPondComment('comment', 'right')
    assert isinstance(comment, marktools.LilyPondComment)


def test_marktools_LilyPondComment___init___03():
    r'''Initialize LilyPond comment from other LilyPond comment.
    '''

    comment_1 = marktools.LilyPondComment('comment')
    comment_2 = marktools.LilyPondComment(comment_1)
    assert comment_1 == comment_2
    assert comment_1 is not comment_2


def test_marktools_LilyPondComment___init___04():
    r'''Initialize LilyPond comment from other LilyPond comment and format slot.
    '''

    comment_1 = marktools.LilyPondComment('comment')
    comment_2 = marktools.LilyPondComment(comment_1, 'after')
    assert comment_1.contents_string == comment_2.contents_string
    assert not comment_1.format_slot == comment_2.format_slot
