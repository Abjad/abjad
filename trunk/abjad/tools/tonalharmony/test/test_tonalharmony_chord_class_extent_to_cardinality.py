from abjad import *
import py.test


def test_tonalharmony_chord_class_extent_to_cardinality_01( ):

   assert tonalharmony.chord_class_extent_to_cardinality(5) == 3 
   assert tonalharmony.chord_class_extent_to_cardinality(7) == 4 
   assert tonalharmony.chord_class_extent_to_cardinality(9) == 5 
   assert tonalharmony.chord_class_extent_to_cardinality(11) == 6 
   assert tonalharmony.chord_class_extent_to_cardinality(13) == 7 


def test_tonalharmony_chord_class_extent_to_cardinality_02( ):

   assert py.test.raises(TonalHarmonyError,
      'tonalharmony.chord_class_extent_to_cardinality(1)')
