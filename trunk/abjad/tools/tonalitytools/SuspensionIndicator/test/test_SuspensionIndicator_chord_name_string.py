from abjad import *


def test_SuspensionIndicator_chord_name_string_01( ):

   t = tonalitytools.SuspensionIndicator(4, 3)
   assert t.chord_name_string == 'sus4'

   t = tonalitytools.SuspensionIndicator(('flat', 2), 1)
   assert t.chord_name_string == 'susb2'

   t = tonalitytools.SuspensionIndicator( )
   assert t.chord_name_string == ''
