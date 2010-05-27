from abjad import *


def test_beam_interface_unspan_01( ):
   '''BeamInterface unspan( ) clears any beam spanner attaching to leaf t.'''

   t = Staff(construct.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Staff {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   t[0].beam.unspan( )

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"

   assert len(p) == 0
   assert not t[0].beam.spanned
   assert not t[1].beam.spanned
   assert not t[2].beam.spanned
   assert not t[3].beam.spanned


def test_beam_interface_unspan_02( ):
   '''t.beam.unspan( ) clears any beam spanner attaching to container t.'''

   t = Staff(Container(construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[ : ]) 

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
   
   t[0].beam.unspan( )

   r'''
   \new Staff {
      {
         c'8
         d'8
      }
      {
         e'8
         f'8
      }
   }
   '''

   assert t.format == "\\new Staff {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n}"

   assert not t[0].beam.spanned
   assert not t[1].beam.spanned
   assert len(p) == 0
