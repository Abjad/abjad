from abjad import *
from abjad.component.component import _Component
import py.test

def test_parentage_signature_01( ):
   '''An anonymous Staff and it's contained unvoiced leaves share the 
   same parentage signature.'''
   t = Staff(construct.scale(4))

   containment = t.parentage.signature
   for component in iterate.naive_forward_in(t, _Component):
      assert component.parentage.signature == containment


def test_parentage_signature_02( ):
   '''A named Staff and it's contained unvoiced leaves share the 
   same parentage signature.'''

   t = Staff(construct.scale(4))
   t.name = 'foo'

   containment = t.parentage.signature
   for component in iterate.naive_forward_in(t, _Component):
      assert component.parentage.signature == containment


def test_parentage_signature_03( ):
   '''Leaves inside equally named sequential voices inside a Staff 
   share the same parentage signature.'''

   t = Staff(Voice(construct.scale(4)) * 2)
   t[0].name = 'foo'
   t[1].name = 'foo'

   containment = t[0][0].parentage.signature
   for leaf in t.leaves:
      assert leaf.parentage.signature == containment


def test_parentage_signature_04( ):
   '''Return _ContainmentSignature giving the root and
      first voice, staff and score in the parentage of component.'''

   t = Voice(construct.run(4))
   t.insert(2, Container(Voice(construct.run(2)) * 2))
   t[2].parallel = True
   pitchtools.diatonicize(t)
   t.note_head.color = 'red'

   r'''
   \new Voice \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   \new Voice {
                           e'8
                           f'8
                   }
                   \new Voice {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }
   '''

   signatures = [leaf.parentage.signature for leaf in t.leaves]

   assert signatures[0] == signatures[1]
   assert signatures[0] != signatures[2]
   assert signatures[0] != signatures[4]
   assert signatures[0] == signatures[6]
   
   assert signatures[2] == signatures[3]
   assert signatures[2] != signatures[4]

      
def test_parentage_signature_05( ):
   '''Unicorporated leaves carry different parentage signatures.'''

   t1 = Note(0, (1, 8))
   t2 = Note(0, (1, 8))
  
   assert t1.parentage.signature != t2.parentage.signature


def test_parentage_signature_06( ):
   '''Leaves inside different Staves with the same name have the same
   parentage signature.'''
   t = Container(Staff(construct.run(2)) * 2)
   t[0].name = t[1].name = 'staff'

   r'''
   {
           \context Staff = "staff" {
                   c'8
                   c'8
           }
           \context Staff = "staff" {
                   c'8
                   c'8
           }
   }
   '''

   assert t.leaves[0].parentage.signature == t.leaves[1].parentage.signature
   assert t.leaves[0].parentage.signature == t.leaves[2].parentage.signature
   assert t.leaves[2].parentage.signature == t.leaves[3].parentage.signature
   assert t.leaves[2].parentage.signature == t.leaves[0].parentage.signature

   assert t[0].parentage.signature == t[1].parentage.signature
