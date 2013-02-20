from abjad.tools import iterationtools
from abjad.tools import layouttools
from abjad.tools import stafftools


def apply_additional_layout(lilypond_file):
    '''Configure multiple-voice rhythmic staves in `lilypond_file`.

    Operate in place and return none.
    '''

    # configure multiple-voice rhythmic staves
    for staff in iterationtools.iterate_staves_in_expr(lilypond_file.score_block[0]):
        if staff.is_parallel:
            assert len(staff) == 2
            voice_1 = staff[0]
            voice_1.override.note_head.Y_offset = 0.5
            voice_1.override.stem.direction = Up
            voice_2 = staff[1]
            voice_2.override.note_head.Y_offset = -0.5
            voice_2.override.stem.direction = Down 
            spacing_vector = layouttools.make_spacing_vector(0, 0, 6, 0)
            staff.override.vertical_axis_group.staff_staff_spacing = spacing_vector

    # provide more space between staves with pitched notes
    for staff in iterationtools.iterate_staves_in_expr(lilypond_file.score_block[0]):
        if not isinstance(staff, stafftools.RhythmicStaff):
            for context_block in lilypond_file.layout_block.context_blocks:
                if context_block.context_name == 'StaffGroup':
                    staff_group_context_block = context_block
                    break
            else:
                raise Exception('no staff group context block found.')
            spacing_vector = layouttools.make_spacing_vector(0, 0, 6, 0)
            context_block.override.vertical_axis_group.staff_staff_spacing = spacing_vector
        break
