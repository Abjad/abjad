from abjad import *
import py.test


def test_Staff_meter_01( ):
   '''Force meter on nonempty staff.'''

   t = Staff(Note(0, (1, 4)) * 8)
   marktools.TimeSignatureMark(2, 4)(t)
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


def test_Staff_meter_02( ):
   '''Force meter on empty staff.'''

   t = Staff([ ])
   marktools.TimeSignatureMark(2, 4)(t)

   r'''
   \new Staff {
      \time 2/4
   }
   '''

   py.test.skip('fix and print meter on empty staff.')
   assert t.format == '\\new Staff {\n\t\\time 2/4\n}'


def test_Staff_meter_03( ):
   '''Staff meter carries over to staff-contained leaves.'''

   t = Staff(Note(0, (1, 4)) * 8)
   marktools.TimeSignatureMark(2, 4)(t)
   for x in t:
      assert marktools.get_effective_time_signature(x) == marktools.TimeSignatureMark(2, 4)


def test_Staff_meter_05( ):
   '''Staff meter set and then clear.
   '''

   t = Staff(Note(0, (1, 4)) * 8)
   marktools.TimeSignatureMark(2, 4)(t)
   marktools.get_effective_time_signature(t).detach_mark( )
   for leaf in t:
      assert marktools.get_effective_time_signature(leaf) is None
