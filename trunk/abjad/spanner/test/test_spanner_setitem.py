from abjad import *


def test_setitem_01( ):
   '''
   Extend spanner at left.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[1])

   r'''
   \new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }
   '''

   p[0 : 0] = (t[0], )

   r'''
   \new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
   assert check(t)


def test_setitem_02( ):
   '''
   Reset all spanner contents.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[1])

   r'''
   \new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }
   '''

   p[ : ] = t[ : ]

   r'''
   \new Voice {
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
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
   assert check(t)
