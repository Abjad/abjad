from abjad import *
import py.test


def test_tonalharmony_chord_class_extent_to_extent_name_01( ):

   assert tonalharmony.chord_class_extent_to_extent_name(5) == 'triad'
   assert tonalharmony.chord_class_extent_to_extent_name(7) == 'seventh'
   assert tonalharmony.chord_class_extent_to_extent_name(9) == 'ninth'
   assert tonalharmony.chord_class_extent_to_extent_name(11) == 'eleventh'
   assert tonalharmony.chord_class_extent_to_extent_name(13) == 'thirteenth'


def test_tonalharmony_chord_class_extent_to_extent_name_02( ):

   assert py.test.raises(TonalHarmonyError,
      'tonalharmony.chord_class_extent_to_extent_name(1)')
