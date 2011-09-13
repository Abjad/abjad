from abjad import *


def test_marktools_get_lilypond_comments_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    comment_mark_1 = marktools.LilyPondComment('comment 1')(staff[0])
    comment_mark_2 = marktools.LilyPondComment('comment 2')(staff[0])

    r'''
    \new Staff {
        %% comment 1
        %% comment 2
        c'8
        d'8
        e'8
        f'8
    }
    '''

    marks = marktools.get_lilypond_comments_attached_to_component(staff[0])

    assert comment_mark_1 in marks
    assert comment_mark_2 in marks
    assert len(marks) == 2
