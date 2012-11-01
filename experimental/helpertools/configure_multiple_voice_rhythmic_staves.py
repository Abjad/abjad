from abjad.tools import iterationtools
from abjad.tools import layouttools


def configure_multiple_voice_rhythmic_staves(lilypond_file):
    '''.. versionadded:: 1.0

    Configure multiple voice rhythmic staves in `score`.

    Operate in place and return none.
    '''

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
