from abjad import *
import py.test


def test_split_unfractured_at_index_01( ):
   '''Index split tuplet in score and do not fracture spanners.'''

   t = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

   r'''\new Voice {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }'''

   split.unfractured_at_index(t[1], 1)

   r'''\new Voice {
           \times 2/3 {
                   c'8 [
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
           }
           \times 2/3 {
                   g'8
                   a'8 ]
           }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t}\n\t\\times 2/3 {\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_split_unfractured_at_index_02( ):
   '''Index split binary measure in score and do not fracture spanners.'''

   t = Voice(RigidMeasure((3, 8), construct.run(3)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

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

   split.unfractured_at_index(t[1], 1)

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
         f'8
      }
      {
         \time 2/8
         g'8
         a'8 ]
      }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\time 1/8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"



def test_split_unfractured_at_index_03( ):
   '''Index split nonbinary measure in score and do not frature spanners.'''

   t = Voice(RigidMeasure((3, 9), construct.run(3)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

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

   split.unfractured_at_index(t[1], 1)

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
            f'8
         }
      }
      {
         \time 2/9
         \scaleDurations #'(8 . 9) {
            g'8
            a'8 ]
         }
      }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t}\n\t{\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8\n\t\t}\n\t}\n\t{\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8\n\t\t\ta'8 ]\n\t\t}\n\t}\n}"


def test_split_unfractured_at_index_04( ):
   '''A single container can be index split in two by the middle;
      no parent.'''

   t = Voice(construct.scale(4))
   t1, t2 = split.unfractured_at_index(t, 2)

   r'''\new Voice {
      c'8
      d'8
   }
   \new Voice {
      e'8
      f'8
   }'''

   assert check.wf(t1)
   assert check.wf(t2)
   assert t1.format == "\\new Voice {\n\tc'8\n\td'8\n}"
   assert t2.format == "\\new Voice {\n\te'8\n\tf'8\n}"
   

def test_split_unfractured_at_index_05( ):
   '''A single container 'split' at index 0 gives
      an empty lefthand part and a complete righthand part.
      Original container empties contents.'''

   t = Staff([Voice(construct.scale(4))])
   v = t[0]
   Beam(v)
   left, right = split.unfractured_at_index(v, 0)

   r'''\new Staff {
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
   }'''

   assert check.wf(t)
   assert left.format == '\\new Voice {\n}'
   assert right.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_split_unfractured_at_index_06( ):
   '''Split container at index > len(container).
      Lefthand part instantiates with all contents.
      Righthand part instantiates empty.
      Original container empties contents.'''

   t = Staff([Voice(construct.scale(4))])
   v = t[0]
   left, right = split.unfractured_at_index(v, 10)

   assert check.wf(t)
   assert left.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
   assert right.format == '\\new Voice {\n}'
   assert v.format == '\\new Voice {\n}'
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_split_unfractured_at_index_07( ):
   '''Voice can be index split.'''

   t = Staff([Voice(construct.scale(4))])
   v = t[0]
   #assert py.test.raises(ContiguityError, 'split.unfractured_at_index(v, -2)')

   left, right = split.unfractured_at_index(v, -2)
   assert check.wf(t)
   assert left.format == "\\new Voice {\n\tc'8\n\td'8\n}"
   assert right.format == "\\new Voice {\n\te'8\n\tf'8\n}"
   assert v.format == '\\new Voice {\n}'
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8\n\t\td'8\n\t}\n\t\\new Voice {\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_split_unfractured_at_index_08( ):
   '''Index split container in score and do not fracture spanners.'''

   t = Staff([Container(construct.scale(4))])
   v = t[0]
   Beam(v)
   left, right = split.unfractured_at_index(v, 2)

   r'''\new Staff {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }'''

   assert check.wf(t)
   assert left.format == "{\n\tc'8 [\n\td'8\n}"
   assert right.format == "{\n\te'8\n\tf'8 ]\n}"
   assert v.format == '{\n}'
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_split_unfractured_at_index_09( ):
   '''Index split tuplet in score and do not fracture spanners.'''

   t = Staff([Voice([FixedMultiplierTuplet((4, 5), construct.run(5))])])
   v = t[0]
   tuplet = v[0]
   Beam(tuplet)
   left, right = split.unfractured_at_index(tuplet, 2)

   r'''\new Staff {
           \new Voice {
                   \times 4/5 {
                           c'8 [
                           c'8
                   }
                   \times 4/5 {
                           c'8
                           c'8
                           c'8 ]
                   }
           }
   }'''

   assert check.wf(t)
   assert left.format == "\\times 4/5 {\n\tc'8 [\n\tc'8\n}"
   assert right.format == "\\times 4/5 {\n\tc'8\n\tc'8\n\tc'8 ]\n}"
   assert tuplet.format == '\\times 4/5 {\n}'
   assert v.format == "\\new Voice {\n\t\\times 4/5 {\n\t\tc'8 [\n\t\tc'8\n\t}\n\t\\times 4/5 {\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\t\\times 4/5 {\n\t\t\tc'8 [\n\t\t\tc'8\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8 ]\n\t\t}\n\t}\n}"


def test_split_unfractured_at_duration_10( ):
   '''Index split left of leaf in score and do not fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2) 
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
   left, right = split.unfractured_at_index(leaf, -100)

   "Score is unchanged."

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

   assert check.wf(t)
   assert left is None
   assert right is leaf
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_split_unfractured_at_duration_11( ):
   '''Index split right of leaf in score and do not fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2) 
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
   left, right = split.unfractured_at_index(leaf, 100)

   "Score is unchanged."

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

   assert check.wf(t)
   assert left is leaf
   assert right is None
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"
