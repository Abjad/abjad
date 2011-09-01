from abjad import *


def test_marktools_attach_lilypond_comments_to_components_in_expr_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    lilypond_comment = marktools.LilyPondComment('foo', 'right')
    marktools.attach_lilypond_comments_to_components_in_expr(staff.leaves, [lilypond_comment])

    r'''
    \new Staff {
        c'8 % foo
        d'8 % foo
        e'8 % foo
        f'8 % foo
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 % foo\n\td'8 % foo\n\te'8 % foo\n\tf'8 % foo\n}"
