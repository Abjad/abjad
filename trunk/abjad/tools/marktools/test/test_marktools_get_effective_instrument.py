from abjad import *


def test_marktools_get_effective_instrument_01( ):

   staff = Staff(macros.scale(4))
   marktools.InstrumentMark('Flute', 'Fl.')(staff)

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   flute = marktools.InstrumentMark('Flute', 'Fl.')
   assert marktools.get_effective_instrument(staff) == flute
   assert marktools.get_effective_instrument(staff[0]) == flute
   assert marktools.get_effective_instrument(staff[1]) == flute
   assert marktools.get_effective_instrument(staff[2]) == flute
   assert marktools.get_effective_instrument(staff[3]) == flute
