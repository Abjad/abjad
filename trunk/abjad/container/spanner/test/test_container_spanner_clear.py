from abjad import *


def test_spanners_01( ):
   '''Clear one spanner attaching to container.'''

   t = Voice(Container(run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"

   t[0].spanners.clear( )

   r'''\new Voice {
      {
         c'8
         d'8
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

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"


def test_clear_02( ):
   '''Clear multiple spanners attaaching to container.'''

   t = Voice(Container(run(2)) * 3)
   pitchtools.diatonicize(t)
   p1 = Beam(t[:])
   p2 = Trill(t[ : ])
   
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
   } '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\startTrillSpan\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ] \\stopTrillSpan\n\t}\n}"

   t[0].spanners.clear( )

   r'''\new Voice {
      {
         c'8
         d'8
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

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
