# -*- coding: utf-8 -*-
from abjad.tools import schemetools


def configure_lilypond_file(lilypond_file):
    r'''Configures LilyPond file.
    '''

    lilypond_file._default_paper_size = '11x17', 'portrait'
    lilypond_file._global_staff_size = 12
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.paper_block.ragged_bottom = True
    spacing_vector = schemetools.make_spacing_vector(0, 0, 8, 0)
    lilypond_file.paper_block.system_system_spacing = spacing_vector