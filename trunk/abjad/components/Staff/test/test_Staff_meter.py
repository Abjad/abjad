from abjad import *
import py.test


def test_Staff_meter_02( ):
   '''Force meter on nonempty staff.'''

   t = Staff(Note(0, (1, 4)) * 8)
   #t.meter.forced = metertools.Meter(2, 4)
   marktools.TimeSignatureMark(2, 4)(Staff, t)
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
   #t.meter.forced = metertools.Meter(2, 4)
   marktools.TimeSignatureMark(2, 4)(Staff, t)

   r'''
   \new Staff {
      \time 2/4
   }
   '''

   py.test.skip('fix and print meter on empty staff.')
   assert t.format == '\\new Staff {\n\t\\time 2/4\n}'


def test_Staff_meter_04( ):
   '''Staff meter carries over to staff-contained leaves.'''

   t = Staff(Note(0, (1, 4)) * 8)
   #t.meter.forced = metertools.Meter(2, 4)
   marktools.TimeSignatureMark(2, 4)(Staff, t)
   for x in t:
      assert x.meter.effective == (2, 4)


#def test_Staff_meter_05( ):
#   '''Staff meterf carries over to staff-contained leaves,
#      but leaves can reassert new meter.'''
#   t = Staff(Note(0, (1, 4)) * 8)
#   t.meter.forced = metertools.Meter(2, 4)
#   t[4].meter.forced = metertools.Meter(4, 4)
#   for i, leaf in enumerate(t):
#      if i in (0, 1, 2, 3):
#         assert leaf.meter.effective == (2, 4)
#      else:
#         assert leaf.meter.effective == (4, 4)


def test_Staff_meter_06( ):
   '''Staff meter set and then clear.
   '''

   t = Staff(Note(0, (1, 4)) * 8)
   #t.meter.forced = metertools.Meter(2, 4)
   #t.meter.forced = None
   marktools.TimeSignatureMark(2, 4)(Staff, t)
   t.meter.effective.detach_mark( )
   for leaf in t:
      #assert leaf.meter.effective == (4, 4)
      assert leaf.meter.effective is None


#def test_Staff_meter_07( ):
#   '''Staff / first-leaf meter competition resolves
#      in favor of first leaf.'''
#   t = Staff(Note(0, (1, 4)) * 8)
#   t.meter.forced = metertools.Meter(4, 4)
#   t[0].meter.forced = metertools.Meter(2, 4)
#   for leaf in t:
#      assert leaf.meter.effective == (2, 4)
