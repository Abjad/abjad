# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_LilyPondComment___init___01():
    r'''Initializes LilyPond comment from contents string.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff[:])
    comment = indicatortools.LilyPondComment('beginning of note content')
    attach(comment, staff[0])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_indicatortools_LilyPondComment___init___02():
    r'''Initializes LilyPond comment from contents string and format slot.
    '''

    comment = indicatortools.LilyPondComment('comment', 'right')
    assert isinstance(comment, indicatortools.LilyPondComment)


def test_indicatortools_LilyPondComment___init___03():
    r'''Initializes LilyPond comment from other LilyPond comment.
    '''

    comment_1 = indicatortools.LilyPondComment('comment')
    comment_2 = indicatortools.LilyPondComment(comment_1)
    assert comment_1 == comment_2
    assert comment_1 is not comment_2


def test_indicatortools_LilyPondComment___init___04():
    r'''Initializes LilyPond comment from other LilyPond comment
    and format slot.
    '''

    comment_1 = indicatortools.LilyPondComment('comment')
    comment_2 = indicatortools.LilyPondComment(comment_1, 'after')
    assert comment_1.contents_string == comment_2.contents_string
    assert not comment_1.format_slot == comment_2.format_slot