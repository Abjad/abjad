from abjad import *


def test_leaf_aggregator_splice_01( ):
   '''Splice components into all attached spanners, after leaf.'''

   t = Voice(scale(4))
   Beam(t[:2])
   Trill(t[:2])

   r'''
   \new Voice {
      c'8 [ \startTrillSpan
      d'8 ] \stopTrillSpan
      e'8
      f'8
   }
   '''
 
   t[1].spanners.splice(t[2:])

   r'''
   \new Voice {
      c'8 [ \startTrillSpan
      d'8
      e'8
      f'8 ] \stopTrillSpan
   }
   '''

   assert check(t)
   assert "\\new Voice {\n\tc'8 [ \\startTrillSpan\n\td'8\n\te'8\n\tf'8 ] \\stopTrillSpan\n}"
