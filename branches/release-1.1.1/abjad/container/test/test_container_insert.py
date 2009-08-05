from abjad import *
import py.test


def test_container_insert_01( ):
   '''Insert component into container at index i.      
      Fracture spanners to the left of index i.
      Fracture spanners to the right of index i.      
      Return Python list of fractured spanners.'''

   "Insert works just before a spanner."

   t = Voice(construct.scale(4))
   Beam(t[:])
   t.insert(0, Rest((1, 8)))

   r'''\new Voice {
           r8
           c'8 [
           d'8
           e'8
           f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tr8\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   
def test_container_insert_02( ):
   '''Insert works inside a spanner.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t.insert(1, Note(1, (1, 8)))

   r'''\new Voice {
      c'8 [
      cs'8
      d'8
      e'8
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tcs'8\n\td'8\n\te'8\n\tf'8 ]\n}"



def test_container_insert_03( ):
   '''Insert works just after a spanner.'''

   t = Staff([Note(n, (1, 8)) for n in range(4)])
   Beam(t[:])
   t.insert(4, Rest((1, 4)))

   r'''\new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
           r4
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\tr4\n}"


def test_container_insert_04( ):
   '''Insert works with really big positive values.'''

   t = Staff([Note(n, (1, 8)) for n in range(4)])
   Beam(t[:])
   t.insert(1000, Rest((1, 4)))

   r'''\new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
        r4
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\tr4\n}"


def test_container_insert_05( ):
   '''Insert works with negative values.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t.insert(-1, Note(4.5, (1, 8)))

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      eqs'8
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\teqs'8\n\tf'8 ]\n}"


def test_container_insert_06( ):
   '''Insert works with really big negative values.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t.insert(-1000, Rest((1, 8)))

   r'''\new Voice {
      r8
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tr8\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_container_insert_07( ):
   '''Inserting a note from one container into another container
      switches note parent from first container to second.'''

   v = Voice(construct.scale(4))
   t = Staff(construct.run(8))
   note = v[0]
   t.insert(1, v[0])

   assert check.wf(v)
   assert check.wf(t)
   assert not note in v
   assert note.parentage.parent is t
