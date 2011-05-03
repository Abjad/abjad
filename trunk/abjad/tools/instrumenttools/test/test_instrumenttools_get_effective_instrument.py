from abjad import *


def test_instrumenttools_get_effective_instrument_01( ):

   staff = Staff("c'8 d'8 e'8 f'8")
   instrumenttools.Flute( )(staff)

   assert isinstance(instrumenttools.get_effective_instrument(staff[0]), instrumenttools.Flute)

