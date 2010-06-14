from abjad import *
import py.test


def test_split_fractured_at_index_01( ):
   '''Index split triplet, and fracture spanners.'''

   t = Voice(FixedDurationTuplet((2, 8), leaftools.make_repeated_notes(3)) * 2)
   tuplet = t[1]
   pitchtools.diatonicize(t)
   Beam(t[:])

   r'''
   \new Voice {
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
   }
   '''

   left, right = split.fractured_at_index(tuplet, 1)

   r'''
   \new Voice {
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
   }
   '''

   assert check.wf(t)
   assert left.format == "\\times 2/3 {\n\tf'8 ]\n}"
   assert right.format == "\\times 2/3 {\n\tg'8 [\n\ta'8 ]\n}"
   assert tuplet.format == ''
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8 ]\n\t}\n\t\\times 2/3 {\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_split_fractured_at_index_02( ):
   '''Index split binary measure, and fracture spanners.'''

   t = Voice(RigidMeasure((3, 8), leaftools.make_repeated_notes(3)) * 2)
   m = t[1]
   Beam(t[:])
   pitchtools.diatonicize(t)

   r'''
   \new Voice {
      {
         \time 3/8
         c'8 [
         d'8
         e'8
      }
      {
         \time 3/8
         f'8
         g'8
         a'8 ]
      }
   }
   '''

   left, right = split.fractured_at_index(m, 1)

   r'''
   \new Voice {
      {
         \time 3/8
         c'8 [
         d'8
         e'8
      }
      {
         \time 1/8
         f'8 ]
      }
      {
         \time 2/8
         g'8 [
         a'8 ]
      }
   }
   '''

   assert check.wf(t)
   assert left.format == "{\n\t\\time 1/8\n\tf'8 ]\n}"
   assert right.format == "{\n\t\\time 2/8\n\tg'8 [\n\ta'8 ]\n}"
   assert py.test.raises(UnderfullMeasureError, 'm.format')
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\time 1/8\n\t\tf'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_split_fractured_at_index_03( ):
   '''Index split nonbinary measure, and fracture spanners.'''

   t = Voice(RigidMeasure((3, 9), leaftools.make_repeated_notes(3)) * 2)
   m = t[1]
   Beam(t[:])
   pitchtools.diatonicize(t)

   r'''
   \new Voice {
      {
         \time 3/9
         \scaleDurations #'(8 . 9) {
            c'8 [
            d'8
            e'8
         }
      }
      {
         \time 3/9
         \scaleDurations #'(8 . 9) {
            f'8
            g'8
            a'8 ]
         }
      }
   }
   '''

   left, right = split.fractured_at_index(m, 1)

   r'''
   \new Voice {
      {
         \time 3/9
         \scaleDurations #'(8 . 9) {
            c'8 [
            d'8
            e'8
         }
      }
      {
         \time 1/9
         \scaleDurations #'(8 . 9) {
            f'8 ]
         }
      }
      {
         \time 2/9
         \scaleDurations #'(8 . 9) {
            g'8 [
            a'8 ]
         }
      }
   }
   '''

   assert check.wf(t)
   assert left.format == "{\n\t\\time 1/9\n\t\\scaleDurations #'(8 . 9) {\n\t\tf'8 ]\n\t}\n}"
   assert right.format == "{\n\t\\time 2/9\n\t\\scaleDurations #'(8 . 9) {\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
   assert py.test.raises(UnderfullMeasureError, 'm.format')
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t}\n\t{\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8 ]\n\t\t}\n\t}\n\t{\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8 [\n\t\t\ta'8 ]\n\t\t}\n\t}\n}"


def test_split_fractured_at_index_04( ):
   '''Index split voice outside of score.
      Fracture spanners.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   left, right = split.fractured_at_index(t, 2)

   r'''
   \new Voice {
           c'8 [
           d'8
   }
   '''

   r'''
   \new Voice {
           e'8
           f'8 ]
   }
   '''

   assert left.format == "\\new Voice {\n\tc'8 [\n\td'8\n}"
   assert right.format == "\\new Voice {\n\te'8\n\tf'8 ]\n}"
   assert t.format == '\\new Voice {\n}'


def test_split_fractured_at_index_05( ):
   '''A single container 'split' at index 0 gives
      an empty lefthand part and a complete righthand part.
      Original container empties contents.'''

   t = Staff([Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))])
   v = t[0]
   Beam(v)

   r'''
   \new Staff {
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
   }
   '''

   left, right = split.fractured_at_index(v, 0)

   r'''
   \new Staff {
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
   }
   '''

   assert left.format == '\\new Voice {\n}'
   assert right.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
   assert v.format == '\\new Voice {\n}'
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_split_fractured_at_index_06( ):
   '''Split container at index > len(container).
      Lefthand part instantiates with all contents.
      Righthand part instantiates empty.
      Original container empties contents.'''

   t = Staff([Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))])
   v = t[0]
   Beam(v)

   left, right = split.fractured_at_index(v, 10)

   r'''
   \new Staff {
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
   }
   '''

   assert left.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
   assert right.format == '\\new Voice {\n}'
   assert v.format == '\\new Voice {\n}'
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_split_fractured_at_index_07( ):
   '''Index split measure in score and fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2) 
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   slur = Slur(t.leaves)

   r'''
   \new Staff {
      {
         \time 2/8
         c'8 [ (
         d'8 ]
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''

   left, right = split.fractured_at_index(t[0], 1)

   r'''
   \new Staff {
      {
         \time 1/8
         c'8 [ ] (
      }
      {
         \time 1/8
         d'8 [ ]
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\tc'8 [ ] (\n\t}\n\t{\n\t\t\\time 1/8\n\t\td'8 [ ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_split_fractured_at_index_08( ):
   '''Index split left of leaf in score and fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2) 
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   slur = Slur(t.leaves)

   r'''
   \new Staff {
      {
         \time 2/8
         c'8 [ (
         d'8 ]
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''

   leaf = t.leaves[1]
   left, right = split.fractured_at_index(leaf, -100)

   r'''
   \new Staff {
      {
         \time 2/8
         c'8 ( ) [
         d'8 ] (
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''
   
   assert check.wf(t)
   assert left is None
   assert right is leaf
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 ( ) [\n\t\td'8 ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"

   
def test_split_fractured_at_index_09( ):
   '''Index split right of leaf in score and fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2) 
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   slur = Slur(t.leaves)

   r'''
   \new Staff {
      {
         \time 2/8
         c'8 [ (
         d'8 ]
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''

   leaf = t.leaves[1]
   left, right = split.fractured_at_index(leaf, 100)

   r'''
   \new Staff {
      {
         \time 2/8
         c'8 [ (
         d'8 ] )
      }
      {
         \time 2/8
         e'8 [ (
         f'8 ] )
      }
   }
   '''

   assert check.wf(t)
   assert left is leaf
   assert right is None
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ] )\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [ (\n\t\tf'8 ] )\n\t}\n}"


def test_split_fractured_at_index_10( ):
   '''Index split nonbinary measure in score.
      Fractured spanners but do not tie over split locus.
      Measure contents necessitate denominator change.'''

   t = Staff([RigidMeasure((3, 12), leaftools.make_first_n_notes_in_ascending_diatonic_scale(2, Rational(3, 16)))])
   Beam(t[0])
   Slur(t.leaves)

   r'''
   \new Staff {
      {
         \time 3/12
         \scaleDurations #'(2 . 3) {
            c'8. [ (
            d'8. ] )
         }
      }
   }
   '''

   halves = split.fractured_at_index(t[0], 1)
   
   r'''
   \new Staff {
      {
         \time 3/24
         \scaleDurations #'(2 . 3) {
            c'8. [ ] (
         }
      }
      {
         \time 3/24
         \scaleDurations #'(2 . 3) {
            d'8. [ ] )
         }
      }
   }
   '''

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8. [ ] (\n\t\t}\n\t}\n\t{\n\t\t\\time 3/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8. [ ] )\n\t\t}\n\t}\n}"


def test_split_fractured_at_index_11( ):
   '''Index split binary measure in score.
      Fractured spanners but do not tie over split locus.
      Measure contents necessitate denominator change.'''

   t = Staff([RigidMeasure((3, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(2, Rational(3, 16)))])
   Beam(t[0])
   Slur(t.leaves)

   r'''
   \new Staff {
      {
         \time 3/8
         c'8. [ (
         d'8. ] )
      }
   }
   '''

   halves = split.fractured_at_index(t[0], 1)

   r'''
   \new Staff {
      {
         \time 3/16
         c'8. [ ] (
      }
      {
         \time 3/16
         d'8. [ ] )
      }
   }
   '''

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\tc'8. [ ] (\n\t}\n\t{\n\t\t\\time 3/16\n\t\td'8. [ ] )\n\t}\n}"
