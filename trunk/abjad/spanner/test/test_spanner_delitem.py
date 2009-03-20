from abjad import *
import py.test


py.test.skip('Spanner changes.')

def test_spanner_delitem_01( ):
   '''
   Delete at nonnegative index in spanner.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[ : ])

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

   del(p[0])

   r'''
   \new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8 [\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
   assert check(t)


def test_spanner_delitem_02( ):
   '''
   Delete at negative index in spanner.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[ : ])

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

   del(p[-1])

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


def test_spanner_delitem_03( ):
   '''
   Delete slice from spanner.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[ : ])

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

   del(p[-2 : ])

   r'''
   \new Voice {
      {
         c'8 [
         d'8 ]
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
   assert check(t)


def test_spanner_delitem_04( ):
   '''
   Delete all spanner components.

   Equivalent to p.clear( ).
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[ : ])

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

   del(p[ : ])

   r'''
   \new Voice {
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
   }
   '''
   
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
   assert check(t)
