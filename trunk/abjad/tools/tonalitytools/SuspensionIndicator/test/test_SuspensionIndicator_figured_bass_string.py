from abjad import *


def test_SuspensionIndicator_figured_bass_string_01( ):

   t = tonalitytools.SuspensionIndicator(4, 3)
   assert t.figured_bass_string == '4-3'

   t = tonalitytools.SuspensionIndicator(('flat', 2), 1)
   assert t.figured_bass_string == 'b2-1'

   t = tonalitytools.SuspensionIndicator( )
   assert t.figured_bass_string == ''
