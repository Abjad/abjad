from abjad import *


def test_meter_interface_effective_01( ):
   '''The default effective meter is 4/4.'''

   t = Staff(construct.scale(4))

   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8
   }'''
   
   for leaf in t:
      assert leaf.meter.effective == Meter(4, 4)


def test_meter_interface_effective_02( ):
   '''Forced meter settings propagate to later leaves.'''

   t = Staff(construct.scale(4))
   t[0].meter.forced = Meter(2, 8)

   r'''\new Staff {
      \time 2/8
      c'8
      d'8
      e'8
      f'8
   }'''

   for leaf in t:
      assert leaf.meter.effective == Meter(2, 8)


def test_meter_interface_effective_03( ):
   '''Setting and then clearing works as expected.'''

   t = Staff(construct.scale(4))
   t[0].meter.forced = Meter(2, 8)
   t[0].meter.forced = None

   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8
   }'''

   for leaf in t:
      assert leaf.meter.effective == Meter(4, 4)
