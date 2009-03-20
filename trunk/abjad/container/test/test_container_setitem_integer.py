from abjad import *
import py.test


def test_container_setitem_integer_01( ):
   '''Spanned leaves exchange correctly.'''

   t = Voice(scale(4))
   Beam(t[:2])
   Glissando(t.leaves)

   r'''\new Voice {
      c'8 [ \glissando
      d'8 ] \glissando
      e'8 \glissando
      f'8
   }'''

   t[1] = Note(12, (1, 8))

   r'''\new Voice {
      c'8 [ \glissando
      c''8 ] \glissando
      e'8 \glissando
      f'8
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\tc''8 ] \\glissando\n\te'8 \\glissando\n\tf'8\n}"


def test_container_setitem_integer_02( ):
   '''Spanned leaf hands position over to container correctly.'''

   t = Voice(scale(4))
   Beam(t[:2])
   Glissando(t.leaves)

   r'''\new Voice {
      c'8 [ \glissando
      d'8 ] \glissando
      e'8 \glissando
      f'8
   }'''

   t[1] = Sequential(run(3, Rational(1, 16)))

   r'''\new Voice {
      c'8 [ \glissando
      {
         c'16 \glissando
         c'16 \glissando
         c'16 ] \glissando
      }
      e'8 \glissando
      f'8
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\t{\n\t\tc'16 \\glissando\n\t\tc'16 \\glissando\n\t\tc'16 ] \\glissando\n\t}\n\te'8 \\glissando\n\tf'8\n}"


def test_container_setitem_integer_03( ):
   '''Directly spanned contains hand over correctly to a single leaf.
      Note here that only the sequentials are initially spanned.'''

   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)   
   Beam(t[:])
   Glissando(t[:])
 
   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 ]
      }
   }'''

   t[1] = Note(12, (1, 8))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      c''8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\tc''8 ]\n}"


def test_container_setitem_integer_04( ):
   '''Indirectly spanned containers hand over correctly to a single leaf.
      Notice here that only LEAVES are initially spanned.'''

   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)   
   Beam(t.leaves)
   Glissando(t.leaves)
 
   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 ]
      }
   }'''

   t[1] = Note(12, (1, 8))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      c''8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\tc''8 ]\n}"


def test_container_setitem_integer_05( ):
   '''Directly spanned containers hand over to other containers correctly.'''

   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)   
   Beam(t[:])
   Glissando(t[:])
 
   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 ]
      }
   }'''

   t[1] = FixedDurationTuplet((2, 8), scale(3))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      \times 2/3 {
         c'8 \glissando
         d'8 \glissando
         e'8 ]
      }
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t\\times 2/3 {\n\t\tc'8 \\glissando\n\t\td'8 \\glissando\n\t\te'8 ]\n\t}\n}"


def test_container_setitem_integer_06( ):
   '''Indirectly spanned containers hand over correctly to a single leaf.'''

   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)   
   Beam(t.leaves)
   Glissando(t.leaves)
 
   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 ]
      }
   }'''

   t[1] = Note(12, (1, 8))

   r'''\new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      c''8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\tc''8 ]\n}"
