# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.materials.example_notes.output_material import example_notes


score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(example_notes)
illustration = lilypondfiletools.make_basic_lilypond_file(score)
