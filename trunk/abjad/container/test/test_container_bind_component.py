from abjad import *


def test_container_bind_component_01( ):
   '''Insert component in container music at index i.
      Neither fracture spanners nor insert into spanners.
      With no spanners, bind is the same as insert.
      With spanners, you should follow bind with spanner insert.'''

   notes = scale(4)
   t = Container(notes[0:1] + notes[2:4])
   beam = Beam(t[:])

   r'''
      c'8 [
      e'8
      f'8 ]
   '''

   assert check(t)

   ## bind should be followed by spanner insert
   ## this is the reason that bind is private
   t._bind_component(1, notes[1])
   assert not check(t)

   beam.insert(1, notes[1]) 

   r'''
      c'8 [
      d'8
      e'8
      f'8 ]
   '''

   assert check(t)
   assert t.format == "\tc'8 [\n\td'8\n\te'8\n\tf'8 ]"


def test_container_bind_component_02( ):
   '''When container contents are not spanned, 
      bind is the same as insert
      and need note be followed by spanner insert.'''

   notes = scale(4)
   t = Container(notes[:3])
   Beam(t[:])

   r'''
      c'8 [
      d'8
      e'8 ]
   '''

   assert check(t)
   
   ## bind will not leave container in a bad state in this case
   t._bind_component(3, notes[3])

   r'''
      c'8 [
      d'8
      e'8 ]
      f'8
   '''

   assert check(t)
   assert t.format == "\tc'8 [\n\td'8\n\te'8 ]\n\tf'8"


## PARENTAGE TESTS ##

def test_container_bind_component_03( ):
   v = Voice(scale(4))
   t = Staff(run(8))
   note = v[0]
   t._bind_component(1, v[0])
   assert check(v)
   assert check(t)
   assert not note in v
   assert note.parentage.parent is t
