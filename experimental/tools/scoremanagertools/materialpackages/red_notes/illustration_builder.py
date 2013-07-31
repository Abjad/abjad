# -*- encoding: utf-8 -*-
from abjad import *
from built_in_materials.red_notes.output_material import red_notes


score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(red_notes)
illustration = lilypondfiletools.make_basic_lilypond_file(score)
