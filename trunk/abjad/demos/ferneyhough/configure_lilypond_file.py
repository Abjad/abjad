from abjad import *


def configure_lilypond_file(lilypond_file):
    lilypond_file.default_paper_size = '11x17', 'portrait'
    lilypond_file.global_staff_size = 12
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.paper_block.ragged_bottom = True
    lilypond_file.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 8, 0)

