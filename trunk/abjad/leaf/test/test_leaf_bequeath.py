from abjad import *


def test_leaf_bequeath_01( ):
   '''Bequeath from note to rest.'''

   t = Voice(Container(run(2)) * 3)
   diatonicize(t)
   Beam(t.leaves)   

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

   old = t.leaves[2]
   #old.bequeath(Rest((1, 8)))
   donate(t.leaves[2:3], Rest((1, 8)))

   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         r8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\tr8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_leaf_bequeath_02( ):
   '''Bequeath from note to tuplet.'''

   t = Voice(Container(run(2)) * 3)
   diatonicize(t)
   Glissando(t[:])
   Beam(t.leaves)   

   r'''\new Voice {
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
   }'''
   
   #t[1][0].bequeath(FixedDurationTuplet((1, 8), Note(0, (1, 16)) * 3))
   donate(t[1][:1], FixedDurationTuplet((1, 8), Note(0, (1, 16)) * 3))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         \times 2/3 {
            c'16 \glissando
            c'16 \glissando
            c'16 \glissando
         }
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tc'16 \\glissando\n\t\t\tc'16 \\glissando\n\t\t\tc'16 \\glissando\n\t\t}\n\t\tf'8 \\glissando\n\t}\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"
