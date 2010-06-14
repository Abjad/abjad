from abjad import *
import py.test


def test_container_extend_01( ):
   '''Extend container with list of leaves.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   Beam(t[:])

   r'''
   \new Voice {
           c'8 [
           d'8 ]
   }
   '''

   t.extend(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))

   r'''
   \new Voice {
           c'8 [
           d'8 ]
           c'8
           d'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\tc'8\n\td'8\n}"


def test_container_extend_02( ):
   '''Extend container with contents of other container.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   Beam(t[:])

   r'''
   \new Voice {
           c'8 [
           d'8 ]
   }
   '''

   u = Voice([Note(4, (1, 8)), Note(5, (1, 8))])
   Beam(u[:])
   t.extend(u)

   r'''
   \new Voice {
           c'8 [
           d'8 ]
           e'8 [
           f'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\te'8 [\n\tf'8 ]\n}"


def test_container_extend_03( ):
   '''Extending container with empty list leaves container unchanged.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   Beam(t[:])
   t.extend([ ])

   r'''
   \new Voice {
           c'8 [
           d'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_container_extend_04( ):
   '''Extending one container with empty second container 
      leaves both containers unchanged.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   Beam(t[:])
   t.extend(Voice([ ]))

   r'''
   \new Voice {
           c'8 [
           d'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_container_extend_05( ):
   '''Trying to extend container with noncomponent raises TypeError.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   Beam(t[:])

   assert py.test.raises(TypeError, 't.extend(7)')
   assert py.test.raises(TypeError, "t.extend('foo')")


def test_container_extend_06( ):
   '''Trying to extend container with noncontainer raises TypeError.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   Beam(t[:])

   assert py.test.raises(TypeError, 't.extend(Note(4, (1, 4)))')
   assert py.test.raises(TypeError, "t.extend(Chord([2, 3, 5], (1, 4)))")


def test_container_extend_07( ):
   '''Extend container with partial and 
      spanned contents of other container.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   Beam(t[:])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
   }
   '''

   u = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(u[:])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   t.extend(u[-2:]) 

   "Container t is now ..."

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\te'8\n\tf'8\n}"

   "Container u is now ..."

   r'''
   \new Voice {
      c'8 [
      d'8 ]
   }
   '''

   assert check.wf(u)
   assert u.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_container_extend_08( ):
   '''Extend container with partial and 
      spanned contents of other container.
      Covered span comes with components from donor container.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   Beam(t[:])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
   }
   '''

   u = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(u[:])
   Slur(u[-2:])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8 (
      f'8 ] )
   }
   '''

   t.extend(u[-2:]) 

   "Container t is now ..."

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8 (
      f'8 )
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\te'8 (\n\tf'8 )\n}"

   "Container u is now ..."

   r'''
   \new Voice {
      c'8 [
      d'8 ]
   }
   '''
  
   assert check.wf(u)
   assert u.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"
