from abjad import *


def test_fracture_01( ):
   '''
   Fracture a spanner crossing the leaves of container t either side of t.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t.leaves)

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

   t[1].spanners.fracture( )

   r'''
   \new Voice {
      {
         c'8 [
         d'8 ]
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8 [
         a'8 ]
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
   assert check(t)


def test_fracture_02( ):
   '''
   Fracture a spanner crossing the leaves of container t to the left of t.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t.leaves)

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

   t[1].spanners.fracture('left')

   r'''
   \new Voice {
      {
         c'8 [
         d'8 ]
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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
   assert check(t)


def test_fracture_03( ):
   '''
   Fracture a spanner crossing the leaves of container t to the right of t.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p = Beam(t.leaves)

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

   t[1].spanners.fracture('right')

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
         g'8 [
         a'8 ]
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
   assert check(t)


def test_fracture_04( ):
   '''
   Fracturing nothing does nothing.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)

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

   t[1].spanners.fracture( )

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
   assert check(t)


def test_fracture_05( ):
   '''
   Fracture multiple spanners crossing leaves in t.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p1 = Beam(t.leaves)
   p2 = Trill(t.leaves)

   r'''
   \new Voice {
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
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\startTrillSpan\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ] \\stopTrillSpan\n\t}\n}"
   assert check(t)

   t[1].spanners.fracture( )

   r'''
   \new Voice {
      {
         c'8 [ \startTrillSpan
         d'8 ] \stopTrillSpan
      }
      {
         e'8 [ \startTrillSpan
         f'8 ] \stopTrillSpan
      }
      {
         g'8 [ \startTrillSpan
         a'8 ] \stopTrillSpan
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\startTrillSpan\n\t\td'8 ] \\stopTrillSpan\n\t}\n\t{\n\t\te'8 [ \\startTrillSpan\n\t\tf'8 ] \\stopTrillSpan\n\t}\n\t{\n\t\tg'8 [ \\startTrillSpan\n\t\ta'8 ] \\stopTrillSpan\n\t}\n}"
   assert check(t)


def test_fracture_06( ):
   '''
   Fracture spanner crossting container t.
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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
   assert check(t)

   t[1].spanners.fracture( )

   r'''
   \new Voice {
      {
         c'8 [
         d'8 ]
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8 [
         a'8 ]
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
   assert check(t)

def test_fracture_07( ):
   '''
   Fracture a spanner crossing container t to the left of t.
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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
   assert check(t)

   t[1].spanners.fracture('left')

   r'''
   \new Voice {
      {
         c'8 [
         d'8 ]
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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
   assert check(t)


def test_fracture_08( ):
   '''
   Fracture a spanner crossing container t to the right of t.
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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
   assert check(t)

   t[1].spanners.fracture('right')

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
         g'8 [
         a'8 ]
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
   assert check(t)
