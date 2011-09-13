from abjad import *


def test_marktools_detach_lilypond_comments_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    marktools.LilyPondComment('comment 1')(staff[0])
    marktools.LilyPondComment('comment 2')(staff[0])

    r'''
    \new Staff {
        % comment 1
        % comment 2
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    marktools.detach_lilypond_comments_attached_to_component(staff[0])

    r'''
    \new Staff {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
