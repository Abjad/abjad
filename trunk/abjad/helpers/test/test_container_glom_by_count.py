from abjad import *


def test_container_glom_by_count_01( ):
   '''Glom voice.'''

   t = Voice(run(5))
   Beam(t)
   container_glom_by_count(t, [1, 2, 2])

   r'''
   \new Voice {
      c'8 [
      c'4
      c'4 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tc'4\n\tc'4 ]\n}"


def test_container_glom_by_count_02( ):
   '''Glom voice and render big-endian tied values.'''

   t = Voice(run(5))
   Beam(t)
   container_glom_by_count(t, [5], direction = 'big-endian')

   r'''
   \new Voice {
      c'2 [ ~
      c'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'2 [ ~\n\tc'8 ]\n}"


def test_container_glom_by_count_03( ):
   '''Glom voice and render big-endian tied values.'''

   t = Voice(run(5))
   Beam(t)
   container_glom_by_count(t, [5], direction = 'little-endian')

   r'''
   \new Voice {
      c'8 [ ~
      c'2 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [ ~\n\tc'2 ]\n}"


def test_container_glom_by_count_04( ):
   '''Glom voice into rests.'''

   t = Voice(run(5))
   container_glom_by_count(t, [1, 2, 2], Rest((1, 4)))

   r'''
   \new Voice {
      r8
      r4
      r4
   }
   '''

   assert check(t)
   assert t.format == '\\new Voice {\n\tr8\n\tr4\n\tr4\n}'
