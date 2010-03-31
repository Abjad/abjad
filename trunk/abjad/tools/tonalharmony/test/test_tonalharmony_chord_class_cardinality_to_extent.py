from abjad import *
import py.test


def test_tonalharmony_chord_class_cardinality_to_extent_01( ):

   assert tonalharmony.chord_class_cardinality_to_extent(3) == 5
   assert tonalharmony.chord_class_cardinality_to_extent(4) == 7
   assert tonalharmony.chord_class_cardinality_to_extent(5) == 9
   assert tonalharmony.chord_class_cardinality_to_extent(6) == 11
   assert tonalharmony.chord_class_cardinality_to_extent(7) == 13


def test_tonalharmony_chord_class_cardinality_to_extent_02( ):

   assert py.test.raises(TonalHarmonyError, 
      'tonalharmony.chord_class_cardinality_to_extent(1)')

   assert py.test.raises(TonalHarmonyError, 
      'tonalharmony.chord_class_cardinality_to_extent(10)')
