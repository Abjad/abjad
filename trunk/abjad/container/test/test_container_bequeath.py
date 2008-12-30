from abjad import *


def test_container_bequeath_01( ):
   '''
   Bequeath from sequential to voice.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   Glissando(t[ : ])
   Beam(t.leaves)
   
   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   old = t[1]

   r'''
   {
      e'8 \glissando
      f'8 \glissando
   }
   '''

   new = Voice( )
   old.bequeath(new)

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t\\new Voice {\n\t\te'8 \\glissando\n\t\tf'8 \\glissando\n\t}\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"

   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      \new Voice {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   assert check(t)

   assert old.format == '{\n}'

   r'''
   {
   }
   '''

   assert new.format == "\\new Voice {\n\te'8 \\glissando\n\tf'8 \\glissando\n}"

   r'''
   \new Voice {
      e'8 \glissando
      f'8 \glissando
   }
   '''

   assert check(new)


def test_container_bequeath_02( ):
   '''
   Bequeath from sequential to tuplet.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   Glissando(t[ : ])
   Beam(t.leaves)
   
   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   t[1].bequeath(FixedDurationTuplet((3, 16), [ ]))

   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      \fraction \times 3/4 {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t\\fraction \\times 3/4 {\n\t\te'8 \\glissando\n\t\tf'8 \\glissando\n\t}\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"

   assert check(t)
