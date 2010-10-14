from abjad import *
from abjad.core import LilyPondContextSettingComponentPlugIn


def test_LilyPondContextSettingComponentPlugIn___repr___01( ):
   '''LilyPond grob proxy repr is evaluable.
   '''

   note = Note(0, (1, 4))
   note.set.staff.tuplet_full_length = True

   context_setting_component_plug_in_1 = note.set
   context_setting_component_plug_in_2 = eval(repr(context_setting_component_plug_in_1))

   assert isinstance(context_setting_component_plug_in_1, LilyPondContextSettingComponentPlugIn)
   assert isinstance(context_setting_component_plug_in_2, LilyPondContextSettingComponentPlugIn)
