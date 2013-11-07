# -*- encoding: utf-8 -*-
from abjad.tools import layouttools
from abjad.tools import scoretools
from abjad.tools.functiontools import iterate
from abjad.tools.functiontools import override


def apply_additional_layout(lilypond_file):
    r'''Configure multiple-voice rhythmic staves in `lilypond_file`.

    Operates in place and returns none.
    '''

    # configure multiple-voice rhythmic staves
    for staff in iterate(lilypond_file.score_block[0]).by_class(Staff):
        if staff.is_simultaneous:
            assert len(staff) == 2
            voice_1 = staff[0]
            override(voice_1).note_head.Y_offset = 0.5
            override(voice_1).stem.direction = Up
            voice_2 = staff[1]
            override(voice_2).note_head.Y_offset = -0.5
            override(voice_2).stem.direction = Down
            spacing_vector = layouttools.make_spacing_vector(0, 0, 6, 0)
            override(staff).vertical_axis_group.staff_staff_spacing = \
                spacing_vector

    # provide more space between staves with pitched notes
    for staff in iterate(lilypond_file.score_block[0]).by_class(Staff):
        if not isinstance(staff, scoretools.RhythmicStaff):
            for context_block in lilypond_file.layout_block.context_blocks:
                if context_block.context_name == 'StaffGroup':
                    staff_group_context_block = context_block
                    break
            else:
                raise Exception('no staff group context block found.')
            spacing_vector = layouttools.make_spacing_vector(0, 0, 6, 0)
            override(context_block).vertical_axis_group.staff_staff_spacing = \
                spacing_vector
        break
