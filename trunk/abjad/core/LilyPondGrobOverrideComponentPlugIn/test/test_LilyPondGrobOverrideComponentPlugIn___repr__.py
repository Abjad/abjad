from abjad import *
from abjad.core import LilyPondGrobOverrideComponentPlugIn


def test_LilyPondGrobOverrideComponentPlugIn___repr___01( ):
   '''LilyPond grob override component plug-in repr is evaluable.
   '''

   note = Note(0, (1, 4))
   note.override.note_head.color = 'red'

   grob_override_component_plug_in_1 = note.override
   grob_override_component_plug_in_2 = eval(repr(grob_override_component_plug_in_1))

   assert isinstance(grob_override_component_plug_in_1, LilyPondGrobOverrideComponentPlugIn)
   assert isinstance(grob_override_component_plug_in_2, LilyPondGrobOverrideComponentPlugIn)
