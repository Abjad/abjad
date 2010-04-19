from abjad import *


def test_SuspensionIndicator_title_string_01( ):

   t = tonalharmony.SuspensionIndicator(4, 3)
   assert t.title_string == 'FourThreeSuspension'

   t = tonalharmony.SuspensionIndicator(('flat', 2), 1)
   assert t.title_string == 'FlatTwoOneSuspension'

   t = tonalharmony.SuspensionIndicator( )
   assert t.title_string == ''
