from abjad import *


def test_container_remove_01( ):
   '''Containers remove leaves correctly.
      Leaf detaches from parentage.
      Leaf withdraws from crossing spanners.
      Leaf carries covered spanners forward.
      Leaf returns after removal.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Slur(t[:])
   Beam(t[1])

   r'''
   \new Voice {
      c'8 (
      d'8 [ ]
      e'8
      f'8 )
   }
   '''

   result = t.remove(t[1])

   r'''
    \new Voice {
      c'8 (
      e'8
      f'8 )
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 (\n\te'8\n\tf'8 )\n}"

   "Result is now d'8 [ ]"

   assert check.wf(result)
   assert result.format == "d'8 [ ]"


def test_container_remove_02( ):
   '''Containers remove nested containers correctly.
      Container detaches from parentage.
      Container withdraws from crossing spanners.
      Container carries covered spanners forward.
      Container returns after removal.'''

   t = Staff(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)
   sequential = t[0]
   p = Beam(t[:])

   r'''
   \new Staff {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }
   '''

   t.remove(sequential)

   r'''
   \new Staff {
      {
         e'8 [
         f'8 ]
      }
   }
   '''
 
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n}"

   r'''
   {
      c'8
      d'8
   }
   '''
   
   assert check.wf(sequential)
   assert sequential.format == "{\n\tc'8\n\td'8\n}"
