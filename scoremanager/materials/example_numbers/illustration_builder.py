from abjad import *
from scoremanager.materials.example_numbers.output_material import example_numbers


notes = scoretools.make_notes(example_numbers, [Duration(1, 8)])
result = scoretools.make_piano_score_from_leaves(notes)
score, treble_staff, bass_staff = result
illustration = lilypondfiletools.make_basic_lilypond_file(score)
