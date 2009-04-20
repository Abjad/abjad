from abjad import *
import py.test


def test_split_container_fractured_01( ):
   '''Split beamed triplet.'''

   t = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
   tuplet = t[1]
   pitchtools.diatonicize(t)
   Beam(t[:])

   r'''\new Voice {
           \times 2/3 {
                   c'8 [
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8 ]
           }
   }'''

   left, right = split.container_fractured(tuplet, 1)

   r'''\new Voice {
           \times 2/3 {
                   c'8 [
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8 ]
           }
           \times 2/3 {
                   g'8 [
                   a'8 ]
           }
   }'''

   assert check.wf(t)
   assert left.format == "\\times 2/3 {\n\tf'8 ]\n}"
   assert right.format == "\\times 2/3 {\n\tg'8 [\n\ta'8 ]\n}"
   assert tuplet.format == ''
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8 ]\n\t}\n\t\\times 2/3 {\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_split_container_fractured_02( ):
   '''Split binary measure.'''

   t = Voice(RigidMeasure((3, 8), construct.run(3)) * 2)
   m = t[1]
   Beam(t[:])
   pitchtools.diatonicize(t)

   r'''\new Voice {
                   \time 3/8
                   c'8 [
                   d'8
                   e'8
                   \time 3/8
                   f'8
                   g'8
                   a'8 ]
   }'''

   left, right = split.container_fractured(m, 1)

   r'''\new Voice {
                   \time 3/8
                   c'8 [
                   d'8
                   e'8
                   \time 1/8
                   f'8 ]
                   \time 2/8
                   g'8 [
                   a'8 ]
   }'''

   assert check.wf(t)
   assert left.format == "\t\\time 1/8\n\tf'8 ]"
   assert right.format == "\t\\time 2/8\n\tg'8 [\n\ta'8 ]"
   assert py.test.raises(UnderfullMeasureError, 'm.format')
   assert t.format == "\\new Voice {\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\t\\time 1/8\n\t\tf'8 ]\n\t\t\\time 2/8\n\t\tg'8 [\n\t\ta'8 ]\n}"


def test_split_container_fractured_03( ):
   '''Split nonbinary measure.'''

   t = Voice(RigidMeasure((3, 9), construct.run(3)) * 2)
   m = t[1]
   Beam(t[:])
   pitchtools.diatonicize(t)

   r'''\new Voice {
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           c'8 [
                           d'8
                           e'8
                   }
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           f'8
                           g'8
                           a'8 ]
                   }
   }'''

   left, right = split.container_fractured(m, 1)

   r'''\new Voice {
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           c'8 [
                           d'8
                           e'8
                   }
                   \time 1/9
                   \scaleDurations #'(8 . 9) {
                           f'8 ]
                   }
                   \time 2/9
                   \scaleDurations #'(8 . 9) {
                           g'8 [
                           a'8 ]
                   }
   }'''

   assert check.wf(t)
   assert left.format == "\t\\time 1/9\n\t\\scaleDurations #'(8 . 9) {\n\t\tf'8 ]\n\t}"
   assert right.format == "\t\\time 2/9\n\t\\scaleDurations #'(8 . 9) {\n\t\tg'8 [\n\t\ta'8 ]\n\t}"
   assert py.test.raises(UnderfullMeasureError, 'm.format')
   assert t.format == "\\new Voice {\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8 ]\n\t\t}\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8 [\n\t\t\ta'8 ]\n\t\t}\n}"


def test_split_container_fractured_04( ):
   '''A single container can be split in two by the middle.
      No parent.'''

   t = Voice(construct.scale(4))
   Beam(t[:])

   r'''\new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }'''

   left, right = split.container_fractured(t, 2)

   r'''\new Voice {
           c'8 [
           d'8
   }'''

   r'''\new Voice {
           e'8
           f'8 ]
   }'''

   assert left.format == "\\new Voice {\n\tc'8 [\n\td'8\n}"
   assert right.format == "\\new Voice {\n\te'8\n\tf'8 ]\n}"
   assert t.format == '\\new Voice {\n}'


def test_split_container_fractured_05( ):
   '''A single container 'split' at index 0 gives
      an empty lefthand part and a complete righthand part.
      Original container empties contents.'''

   t = Staff([Voice(construct.scale(4))])
   v = t[0]
   Beam(v)

   r'''\new Staff {
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
   }'''

   left, right = split.container_fractured(v, 0)

   r'''\new Staff {
           \new Voice {
           }
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
   }'''

   assert left.format == '\\new Voice {\n}'
   assert right.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
   assert v.format == '\\new Voice {\n}'
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t}\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_split_container_fractured_06( ):
   '''Split container at index > len(container).
      Lefthand part instantiates with all contents.
      Righthand part instantiates empty.
      Original container empties contents.'''

   t = Staff([Voice(construct.scale(4))])
   v = t[0]
   Beam(v)

   left, right = split.container_fractured(v, 10)

   r'''\new Staff {
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
           \new Voice {
           }
   }'''

   assert left.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
   assert right.format == '\\new Voice {\n}'
   assert v.format == '\\new Voice {\n}'
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n\t\\new Voice {\n\t}\n}"
