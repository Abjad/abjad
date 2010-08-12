from abjad import *


def test__Leaf_splice_01( ):
   '''Splice leaves after leaf.'''

   t = Voice(macros.scale(3))
   BeamSpanner(t[:])
   result = t[-1].splice(macros.scale(3))

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      c'8
      d'8
      e'8 ]
   }
   '''
   
   assert componenttools.is_well_formed_component(t)
   assert result == t[-4:]
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tc'8\n\td'8\n\te'8 ]\n}"


def test__Leaf_splice_02( ):
   '''Splice leaf after interior leaf.'''

   t = Voice(macros.scale(3))
   BeamSpanner(t[:])
   result = t[1].splice([Note(2.5, (1, 8))])

   r'''
   \new Voice {
           c'8 [
           d'8
           dqs'8
           e'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\tdqs'8\n\te'8 ]\n}"
   assert result == t[1:3]
