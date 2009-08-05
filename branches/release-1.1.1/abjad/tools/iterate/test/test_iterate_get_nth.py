from abjad import *


def test_iterate_get_nth_01( ):

   staff = Staff([ ])
   durations = [Rational(n, 16) for n in range(1, 5)]
   notes = construct.notes([0, 2, 4, 5], durations)
   rests = construct.rests(durations)
   leaves = listtools.interlace(notes, rests)
   staff.extend(leaves)

   r'''\new Staff {
           c'16
           r16
           d'8
           r8
           e'8.
           r8.
           f'4
           r4
   }'''

   assert iterate.get_nth(staff, Note, 0) is notes[0]
   assert iterate.get_nth(staff, Note, 1) is notes[1]
   assert iterate.get_nth(staff, Note, 2) is notes[2]
   assert iterate.get_nth(staff, Note, 3) is notes[3]

   assert iterate.get_nth(staff, Rest, 0) is rests[0]
   assert iterate.get_nth(staff, Rest, 1) is rests[1]
   assert iterate.get_nth(staff, Rest, 2) is rests[2]
   assert iterate.get_nth(staff, Rest, 3) is rests[3]

   assert iterate.get_nth(staff, Staff, 0) is staff


def test_iterate_get_nth_02( ):
   '''Iterates backwards with negative values of n.'''

   staff = Staff([ ])
   durations = [Rational(n, 16) for n in range(1, 5)]
   notes = construct.notes([0, 2, 4, 5], durations)
   rests = construct.rests(durations)
   leaves = listtools.interlace(notes, rests)
   staff.extend(leaves)

   r'''\new Staff {
           c'16
           r16
           d'8
           r8
           e'8.
           r8.
           f'4
           r4
   }'''

   assert iterate.get_nth(staff, Note, -1) is notes[3]
   assert iterate.get_nth(staff, Note, -2) is notes[2]
   assert iterate.get_nth(staff, Note, -3) is notes[1]
   assert iterate.get_nth(staff, Note, -4) is notes[0]

   assert iterate.get_nth(staff, Rest, -1) is rests[3]
   assert iterate.get_nth(staff, Rest, -2) is rests[2]
   assert iterate.get_nth(staff, Rest, -3) is rests[1]
   assert iterate.get_nth(staff, Rest, -4) is rests[0]
