from abjad import *
from experimental.tools.scoremanagertools.built_in_materials.green_music_specifier.output_material import green_music_specifier


score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(green_music_specifier)
illustration = lilypondfiletools.make_basic_lilypond_file(score)