from abjad import *


### TODO - rename die( ) to something less severe

def test_die_01( ):
   '''
   Die a single spanner.
   '''

   t = Voice(scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[0].spanners.die( )

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_die_02( ):
   '''
   Die multiple spanners.
   '''

   t = Voice(scale(4))
   p1 = Beam(t[ : ])
   p2 = Trill(t[ : ])

   r'''
   \new Voice {
      c'8 [ \startTrillSpan
      d'8
      e'8
      f'8 ] \stopTrillSpan
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [ \\startTrillSpan\n\td'8\n\te'8\n\tf'8 ] \\stopTrillSpan\n}"

   t[0].spanners.die( )

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
