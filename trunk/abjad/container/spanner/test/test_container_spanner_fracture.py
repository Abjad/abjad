from abjad import *


def test_container_spanner_fracture_01( ):
   '''Fracture spanner either side of container.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

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

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_container_spanner_fracture_02( ):
   '''Fracture spanner to the left of container.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

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

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"

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

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_container_spanner_fracture_03( ):
   '''Fracture spanner to the right of container.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

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

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"

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

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_container_spanner_fracture_04( ):
   '''Fracturing nothing does nothing.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)

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

   t[1].spanners.fracture( )

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
