from abjad import *


def test_ChordClass_root_string_01( ):

   assert tonalharmony.ChordClass('c', 'major', 'triad').root_string == 'C'
   assert tonalharmony.ChordClass('c', 'minor', 'triad').root_string == 'c'
   assert tonalharmony.ChordClass('cs', 'major', 'triad').root_string == 'C#'
   assert tonalharmony.ChordClass('cs', 'minor', 'triad').root_string == 'c#'
   assert tonalharmony.ChordClass('cf', 'major', 'triad').root_string == 'Cb'
   assert tonalharmony.ChordClass('cf', 'minor', 'triad').root_string == 'cb'
