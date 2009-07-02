from abjad import *
import py.test
py.test.skip('measure redo')


def test_split_fractured_at_duration_01( ):
   '''Duration split leaf in score and fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   halves = split.fractured_at_duration(t.leaves[0], Rational(1, 32))

   r'''\new Staff {
         \time 2/8
         c'32 ( ) [
         c'16. (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   assert isinstance(halves, tuple)
   assert isinstance(halves[0], list)
   assert isinstance(halves[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tc'32 ( ) [\n\t\tc'16. (\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_02( ):
   '''Duration split measure in score and fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   halves = split.fractured_at_duration(t[0], Rational(1, 32))

   r'''\new Staff {
         \time 1/32
         c'32 [ ] ( )
         \time 7/32
         c'16. [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert isinstance(halves, tuple)
   assert isinstance(halves[0], list)
   assert isinstance(halves[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t\t\\time 7/32\n\t\tc'16. [ (\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_03( ):
   '''Duration split staff outside of score and fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   halves = split.fractured_at_duration(t, Rational(1, 32))

   "halves[0][0]"

   r'''\new Staff {
         \time 1/32
         c'32 [ ] ( )
   }'''

   assert halves[0][0].format == "\\new Staff {\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n}"

   "halves[1][0]"

   r'''\new Staff {
         \time 7/32
         c'16. [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert halves[1][0].format == "\\new Staff {\n\t\t\\time 7/32\n\t\tc'16. [ (\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_04( ):
   '''Duration fracture leaf in score at nonzero index.
      Fracture spanners.
      Test comes from a bug fix.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   split.fractured_at_duration(t.leaves[1], Rational(1, 32))

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'32 )
         d'16. ] (
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32 )\n\t\td'16. ] (\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_05( ):
   '''Duration fracture container over leaf at nonzero index.
      Fracture spanners.
      Test results from bug fix.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   split.fractured_at_duration(t[0], Rational(7, 32))

   r'''\new Staff {
         \time 7/32
         c'8 [ (
         d'16. ] )
         \time 1/32
         d'32 [ ] (
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 7/32\n\t\tc'8 [ (\n\t\td'16. ] )\n\t\t\\time 1/32\n\t\td'32 [ ] (\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_06( ):
   '''Duration split container between leaves and fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   parts = split.fractured_at_duration(t[0], Rational(1, 8))

   r'''\new Staff {
         \time 1/8
         c'8 [ ] (
         \time 1/8
         d'8 [ ] (
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert isinstance(parts, tuple)
   assert isinstance(parts[0], list)
   assert isinstance(parts[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 1/8\n\t\tc'8 [ ] ( )\n\t\t\\time 1/8\n\t\td'8 [ ] (\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_07( ):
   '''Duration split leaf outside of score and fracture spanners.'''

   t = Note(0, (1, 8))
   Beam(t)

   "c'8 [ ]"

   halves = split.fractured_at_duration(t, Rational(1, 32))

   "c'32 [ ]"
   assert check.wf(halves[0][0])

   "c'16. [ ]"
   assert check.wf(halves[1][0])


def test_split_fractured_at_duration_08( ):
   '''Duration split leaf in score and fracture spanners.
      Tie leaves after split.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   d = Rational(1, 32)
   halves = split.fractured_at_duration(t.leaves[0], d, tie_after = True)

   r'''\new Staff {
         \time 2/8
         c'32 ( ) [ ~
         c'16. (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   assert isinstance(halves, tuple)
   assert isinstance(halves[0], list)
   assert isinstance(halves[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tc'32 ( ) [ ~\n\t\tc'16. (\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_09( ):
   '''Duration split measure in score and fracture spanners.
      Tie leaves after split.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   d = Rational(1, 32)
   halves = split.fractured_at_duration(t[0], d, tie_after = True)

   r'''\new Staff {
         \time 1/32
         c'32 [ ] ( ) ~
         \time 7/32
         c'16. [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert isinstance(halves, tuple)
   assert isinstance(halves[0], list)
   assert isinstance(halves[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 1/32\n\t\tc'32 [ ] ( ) ~\n\t\t\\time 7/32\n\t\tc'16. [ (\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_10( ):
   '''Duration split binary measure in score at nonbinary split point.
      Do fracture spanners but do not tie leaves after split.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   d = Rational(1, 5)
   halves = split.fractured_at_duration(t[0], d)

   r'''\new Staff {
         \time 4/20
         \scaleDurations #'(4 . 5) {
            c'8 [ ( ~
            c'32
            d'16. ] )
         }
         \time 1/20
         \scaleDurations #'(4 . 5) {
            d'16 [ ] (
         }
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 4/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'8 [ ( ~\n\t\t\tc'32\n\t\t\td'16. ] )\n\t\t}\n\t\t\\time 1/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\td'16 [ ] (\n\t\t}\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_11( ):
   '''Duration split binary measure in score at nonbinary split point.
      Do fracture spanners and do tie leaves after split.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
         \time 2/8
         c'8 [ (
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   d = Rational(1, 5)
   halves = split.fractured_at_duration(t[0], d, tie_after = True)

   r'''\new Staff {
         \time 4/20
         \scaleDurations #'(4 . 5) {
            c'8 [ ( ~
            c'32
            d'16. ] ) ~
         }
         \time 1/20
         \scaleDurations #'(4 . 5) {
            d'16 [ ] (
         }
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 4/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'8 [ ( ~\n\t\t\tc'32\n\t\t\td'16. ] ) ~\n\t\t}\n\t\t\\time 1/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\td'16 [ ] (\n\t\t}\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_fractured_at_duration_12( ):
   '''Split binary measure at nonbinary split point.
      Do fracture spanners but do not tie across split locus.
      This test results from a fix.
      What's being tested here is contents rederivation.'''

   t = Staff(RigidMeasure((3, 8), construct.scale(3)) * 2)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
                   \time 3/8
                   c'8 [ (
                   d'8
                   e'8 ]
                   \time 3/8
                   c'8 [
                   d'8
                   e'8 ] )
   }'''   

   halves = split.fractured_at_duration(t[0], Rational(7, 20))

   r'''\new Staff {
                   \time 14/40
                   \scaleDurations #'(4 . 5) {
                           c'8 [ ( ~
                           c'32
                           d'8 ~
                           d'32
                           e'8 ] )
                   }
                   \time 1/40
                   \scaleDurations #'(4 . 5) {
                           e'32 [ ] (
                   }
                   \time 3/8
                   c'8 [
                   d'8
                   e'8 ] )
   }'''
   
   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 14/40\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'8 [ ( ~\n\t\t\tc'32\n\t\t\td'8 ~\n\t\t\td'32\n\t\t\te'8 ] )\n\t\t}\n\t\t\\time 1/40\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\te'32 [ ] (\n\t\t}\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8 ] )\n}"
   

def test_split_fractured_at_duration_13( ):
   '''Duration split leaf with LilyPond multiplier.
      Split at binary split point.
      Halves carry original written duration.
      Halves carry adjusted LilyPond multipliers.'''

   t = Note(0, (1, 8))
   t.duration.multiplier = Rational(1, 2)

   "c'8 * 1/2"

   halves = split.fractured_at_duration(t, Rational(1, 32))

   assert len(halves) == 2
   assert check.wf(halves[0][0])
   assert check.wf(halves[1][0])

   assert halves[0][0].format == "c'8 * 1/4"
   assert halves[1][0].format == "c'8 * 1/4"


def test_split_fractured_at_duration_14( ):
   '''Duration split leaf with LilyPond multiplier.
      Split at nonbinary split point.
      Halves carry original written duration.
      Halves carry adjusted LilyPond multipliers.'''

   t = Note(0, (1, 8))
   t.duration.multiplier = Rational(1, 2)

   "c'8 * 1/2"

   halves = split.fractured_at_duration(t, Rational(1, 48))

   assert len(halves) == 2
   assert check.wf(halves[0][0])
   assert check.wf(halves[1][0])

   assert halves[0][0].format == "c'8 * 1/6"
   assert halves[1][0].format == "c'8 * 1/3"


def test_split_fractured_at_duration_15( ):
   '''Duration split binary measure with multiplied leaves.
      Split at binary split point between leaves.''
      Leaves remain unaltered.'''

   t = Staff(RigidMeasure((2, 16), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   for leaf in t.leaves:
      leaf.duration.multiplier = Rational(1, 2)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
                   \time 2/16
                   c'8 * 1/2 [ (
                   d'8 * 1/2 ]
                   \time 2/16
                   e'8 * 1/2 [
                   f'8 * 1/2 ] )
   }'''

   halves = split.fractured_at_duration(t[0], Rational(1, 16))

   r'''\new Staff {
                   \time 1/16
                   c'8 * 1/2 [ ] ( )
                   \time 1/16
                   c'8 * 1/2 [ ] (
                   \time 2/16
                   c'8 * 1/2 [
                   c'8 * 1/2 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 1/16\n\t\tc'8 * 1/2 [ ] ( )\n\t\t\\time 1/16\n\t\td'8 * 1/2 [ ] (\n\t\t\\time 2/16\n\t\te'8 * 1/2 [\n\t\tf'8 * 1/2 ] )\n}"


def test_split_fractured_at_duration_16( ):
   '''Duration split binary measure with multiplied leaves.
      Split at binary split point through leaves.
      Leaf written durations stay the same but multipliers change.'''

   t = Staff(RigidMeasure((2, 16), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   for leaf in t.leaves:
      leaf.duration.multiplier = Rational(1, 2)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
                   \time 2/16
                   c'8 * 1/2 [ (
                   d'8 * 1/2 ]
                   \time 2/16
                   e'8 * 1/2 [
                   f'8 * 1/2 ] )
   }'''

   halves = split.fractured_at_duration(t[0], Rational(3, 32))

   r'''\new Staff {
                   \time 3/32
                   c'8 * 1/2 [ (
                   d'8 * 1/4 ] )
                   \time 1/32
                   d'8 * 1/4 [ ] (
                   \time 2/16
                   e'8 * 1/2 [
                   f'8 * 1/2 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 3/32\n\t\tc'8 * 1/2 [ (\n\t\td'8 * 1/4 ] )\n\t\t\\time 1/32\n\t\td'8 * 1/4 [ ] (\n\t\t\\time 2/16\n\t\te'8 * 1/2 [\n\t\tf'8 * 1/2 ] )\n}"


def test_split_fractured_at_duration_17( ):
   '''Duration split binary measure with multiplied leaves.
      Split at nonbinary split point through leaves.
      Leaf written durations adjust for binary-to-nonbinary change.
      Leaf multipliers also change.'''

   t = Staff(RigidMeasure((2, 16), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   for leaf in t.leaves:
      leaf.duration.multiplier = Rational(1, 2)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''\new Staff {
                   \time 2/16
                   c'8 * 1/2 [ (
                   d'8 * 1/2 ]
                   \time 2/16
                   e'8 * 1/2 [
                   f'8 * 1/2 ] )
   }'''

   halves = split.fractured_at_duration(t[0], Rational(2, 24))

   r'''\new Staff {
                   \time 2/24
                   \scaleDurations #'(2 . 3) {
                           c'8. * 1/2 [ (
                           d'8. * 1/6 ] )
                   }
                   \time 1/24
                   \scaleDurations #'(2 . 3) {
                           d'8. * 1/3 [ ] (
                   }
                   \time 2/16
                   e'8 * 1/2 [
                   f'8 * 1/2 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 2/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8. * 1/2 [ (\n\t\t\td'8. * 1/6 ] )\n\t\t}\n\t\t\\time 1/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8. * 1/3 [ ] (\n\t\t}\n\t\t\\time 2/16\n\t\te'8 * 1/2 [\n\t\tf'8 * 1/2 ] )\n}"


def test_split_fractured_at_duration_18( ):
   '''Duration split binary measure with multiplied leaves.
      Meter carries numerator that necessitates ties.
      Split at nonbinary split point through leaves.'''

   t = Staff([RigidMeasure((5, 16), [Skip((1, 1))])])
   t.leaves[0].duration.multiplier = Rational(5, 16)

   r'''\new Staff {
                   \time 5/16
                   s1 * 5/16
   }'''

   halves = split.fractured_at_duration(t[0], Rational(16, 80))

   r'''\new Staff {
                   \time 16/80
                   \scaleDurations #'(4 . 5) {
                           s1 * 1/4
                   }
                   \time 9/80
                   \scaleDurations #'(4 . 5) {
                           s1 * 9/64
                   }
   }'''   

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 16/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\ts1 * 1/4\n\t\t}\n\t\t\\time 9/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\ts1 * 9/64\n\t\t}\n}"


def test_split_fractured_at_duration_19( ):
   '''Duration split nonbinary measure at nonbinary split point.
      Measure multiplier and split point multiplier match.
      Split between leaves but do fracture spanners.'''

   t = Staff([RigidMeasure((15, 80), construct.notes(
      0, [Rational(1, 32)] * 7 + [Rational(1, 64)]))])
   pitchtools.diatonicize(t)
   Beam(t[0])
   Slur(t.leaves)

   r'''\new Staff {
                   \time 15/80
                   \scaleDurations #'(4 . 5) {
                           c'32 [ (
                           d'32
                           e'32
                           f'32
                           g'32
                           a'32
                           b'32
                           c''64 ] )
                   }
   }'''

   halves = split.fractured_at_duration(t[0], Rational(14, 80))

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 14/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'32 [ (\n\t\t\td'32\n\t\t\te'32\n\t\t\tf'32\n\t\t\tg'32\n\t\t\ta'32\n\t\t\tb'32 ] )\n\t\t}\n\t\t\\time 1/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc''64 [ ] ( )\n\t\t}\n}"
