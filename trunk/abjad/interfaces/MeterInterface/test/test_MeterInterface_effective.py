from abjad import *


def test_MeterInterface_effective_01( ):
   #'''The default effective meter is 4/4.'''
   '''The default effective meter is none.'''

   t = Staff(macros.scale(4))

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''
   
   for leaf in t:
      #assert leaf.meter.effective == metertools.Meter(4, 4)
      assert leaf.meter.effective is None


def test_MeterInterface_effective_02( ):
   '''Forced meter settings propagate to later leaves.'''

   t = Staff(macros.scale(4))
   #t[0].meter.forced = metertools.Meter(2, 8)
   marktools.TimeSignatureMark(2, 8)(t[0])

   r'''
   \new Staff {
      \time 2/8
      c'8
      d'8
      e'8
      f'8
   }
   '''

   for leaf in t:
      #assert leaf.meter.effective == metertools.Meter(2, 8)
      assert leaf.meter.effective == marktools.TimeSignatureMark(2, 8)


def test_MeterInterface_effective_03( ):
   '''Setting and then clearing works as expected.'''

   t = Staff(macros.scale(4))
   #t[0].meter.forced = metertools.Meter(2, 8)
   #t[0].meter.forced = None
   time_signature = marktools.TimeSignatureMark(2, 8)(t[0])
   time_signature.detach_mark( )

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   for leaf in t:
      #assert leaf.meter.effective == metertools.Meter(4, 4)
      assert leaf.meter.effective is None
