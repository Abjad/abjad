from abjad import *
import py.test
py.test.skip('skip for the moment.')


def test_componenttools_component_to_pitch_and_rhythm_skeleton_with_interface_attributes_01( ):

   
   note = Note(0, (1, 4))
   note = score.leaves[0]
   note.override.beam.thickness = 3
   note.duration.multiplier = Fraction(1, 2)
   note.override.note_head.color = 'red'

