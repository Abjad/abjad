from abjad import *


def test_container_aggregator_splice_01( ):
   '''Splice components into all attached spanners,
      starting at the index immediately following self.'''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   Beam(t[0])
   Trill(t[0])

   r'''\new Voice {
      {
         c'8 [ \startTrillSpan
         d'8 ] \stopTrillSpan
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8
      }
   }'''

   t[0].spanners._splice(t[1:])

   r'''\new Voice {
      {
         c'8 [ \startTrillSpan
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ] \stopTrillSpan
      }
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\startTrillSpan\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ] \\stopTrillSpan\n\t}\n}"
