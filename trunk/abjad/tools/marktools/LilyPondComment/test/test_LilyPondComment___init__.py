from abjad import *


def test_LilyPondComment___init___01():
    '''Initialize LilyPond comment from contents string.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    lilypond_comment = marktools.LilyPondComment('beginning of note content')(staff[0])

    r'''
    \new Staff {
        % beginning of note content
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t% beginning of note content\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"


def test_LilyPondComment___init___02():
    '''Initialize LilyPond comment from contents string and format slot.
    '''

    lilypond_comment = marktools.LilyPondComment('comment', 'right')
    assert isinstance(lilypond_comment, marktools.LilyPondComment)


def test_LilyPondComment___init___03():
    '''Initialize LilyPond comment from other LilyPond comment.
    '''

    lilypond_comment_1 = marktools.LilyPondComment('comment')
    lilypond_comment_2 = marktools.LilyPondComment(lilypond_comment_1)
    assert lilypond_comment_1 == lilypond_comment_2
    assert lilypond_comment_1 is not lilypond_comment_2


def test_LilyPondComment___init___04():
    '''Initialize LilyPond comment from other LilyPond comment and format slot.
    '''

    lilypond_comment_1 = marktools.LilyPondComment('comment')
    lilypond_comment_2 = marktools.LilyPondComment(lilypond_comment_1, 'after')
    assert lilypond_comment_1.contents_string == lilypond_comment_2.contents_string
    assert not lilypond_comment_1.format_slot == lilypond_comment_2.format_slot
