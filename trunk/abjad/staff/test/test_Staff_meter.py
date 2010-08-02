from abjad import *
from abjad.meter import Meter


def test_Staff_meter_01( ):
   '''Test MeterInterface public attributes.'''
   t = Staff(Note(0, (1, 4)) * 8)
   assert t.meter.change == False
   assert isinstance(t.meter.effective, Meter)
   assert t.meter.forced is None


def test_Staff_meter_02( ):
   '''Force meter on nonempty staff.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.meter.forced = Meter(2, 4)
   assert t.format == "\\new Staff {\n\t\\time 2/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
   r'''
   \new Staff {
      \time 2/4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
   }
   '''


def test_Staff_meter_03( ):
   '''Force meter on empty staff.'''
   t = Staff([ ])
   t.meter.forced = Meter(2, 4)
   assert t.format == '\\new Staff {\n\t\\time 2/4\n}'
   r'''
   \new Staff {
      \time 2/4
   }
   '''


def test_Staff_meter_04( ):
   '''Staff meter carries over to staff-contained leaves.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.meter.forced = Meter(2, 4)
   for x in t:
      assert x.meter.effective == (2, 4)


#def test_Staff_meter_05( ):
#   '''Staff meterf carries over to staff-contained leaves,
#      but leaves can reassert new meter.'''
#   t = Staff(Note(0, (1, 4)) * 8)
#   t.meter.forced = Meter(2, 4)
#   t[4].meter.forced = Meter(4, 4)
#   for i, leaf in enumerate(t):
#      if i in (0, 1, 2, 3):
#         assert leaf.meter.effective == (2, 4)
#      else:
#         assert leaf.meter.effective == (4, 4)


def test_Staff_meter_06( ):
   '''Staff meter clears with None.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.meter.forced = Meter(2, 4)
   t.meter.forced = None
   for leaf in t:
      assert leaf.meter.effective == (4, 4)


#def test_Staff_meter_07( ):
#   '''Staff / first-leaf meter competition resolves
#      in favor of first leaf.'''
#   t = Staff(Note(0, (1, 4)) * 8)
#   t.meter.forced = Meter(4, 4)
#   t[0].meter.forced = Meter(2, 4)
#   for leaf in t:
#      assert leaf.meter.effective == (2, 4)
