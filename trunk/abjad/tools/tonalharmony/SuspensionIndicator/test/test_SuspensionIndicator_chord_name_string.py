from abjad import *


def test_SuspensionIndicator_chord_name_string_01( ):

   t = tonalharmony.SuspensionIndicator(4, 3)
   assert t.chord_name_string == 'sus4'

   t = tonalharmony.SuspensionIndicator(('flat', 2), 1)
   assert t.chord_name_string == 'susb2'

   t = tonalharmony.SuspensionIndicator( )
   assert t.chord_name_string == ''
