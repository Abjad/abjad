from abjad import *


def test_split_unfractured_at_duration_01( ):

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

   halves = split.unfractured_at_duration(t.leaves[0], Rational(1, 32))

   r'''\new Staff {
         \time 2/8
         c'32 [ (
         c'16.
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert isinstance(halves, tuple)
   assert isinstance(halves[0], list)
   assert isinstance(halves[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tc'32 [ (\n\t\tc'16.\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_unfractured_at_duration_02( ):

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

   halves = split.unfractured_at_duration(t[0], Rational(1, 32))

   r'''\new Staff {
         \time 1/32
         c'32 [ (
         \time 7/32
         c'16.
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert isinstance(halves, tuple)
   assert isinstance(halves[0], list)
   assert isinstance(halves[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 1/32\n\t\tc'32 [ (\n\t\t\\time 7/32\n\t\tc'16.\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_unfractured_at_duration_03( ):

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

   halves = split.unfractured_at_duration(t, Rational(1, 32))

   "halves[0][0]"

   r'''\new Staff {
         \time 1/32
         c'32 [ (
   }'''

   assert halves[0][0].format == "\\new Staff {\n\t\t\\time 1/32\n\t\tc'32 [ (\n}"

   "halves[1][0]"

   r'''\new Staff {
         \time 7/32
         c'16.
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert halves[1][0].format == "\\new Staff {\n\t\t\\time 7/32\n\t\tc'16.\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_unfractured_at_duration_04( ):
   '''Duration split one leaf in score.
      Do not fracture spanners. But do tie after split.'''

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
   halves = split.unfractured_at_duration(t.leaves[0], d, tie_after = True)

   r'''\new Staff {
         \time 2/8
         c'32 [ ( ~
         c'16.
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert isinstance(halves, tuple)
   assert isinstance(halves[0], list)
   assert isinstance(halves[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tc'32 [ ( ~\n\t\tc'16.\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_unfractured_at_duration_05( ):
   '''Duration split one measure in score.
      Do not fracture spanners. But do add tie after split.'''

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
   halves = split.unfractured_at_duration(t[0], d, tie_after = True)

   r'''\new Staff {
         \time 1/32
         c'32 [ ( ~
         \time 7/32
         c'16.
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert isinstance(halves, tuple)
   assert isinstance(halves[0], list)
   assert isinstance(halves[1], list)
   assert t.format == "\\new Staff {\n\t\t\\time 1/32\n\t\tc'32 [ ( ~\n\t\t\\time 7/32\n\t\tc'16.\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"


def test_split_unfractured_at_duration_06( ):
   '''Duration split binary measure in score at nonbinary split point.
      Do not fracture spanners and do not tie leaves after split.'''

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
   halves = split.unfractured_at_duration(t[0], d)

   r'''\new Staff {
         \time 4/20
         \scaleDurations #'(4 . 5) {
            c'8 [ ( ~
            c'32
            d'16. ~ # tie here is bug
         }
         \time 1/20
         \scaleDurations #'(4 . 5) {
            d'16 ]
         }
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   ## TODO: The tie at the split locus here is a (small) bug. ##
   ##       Eventually should fix. ##


def test_split_unfractured_at_duration_07( ):
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
   halves = split.unfractured_at_duration(t[0], d, tie_after = True)

   r'''\new Staff {
         \time 4/20
         \scaleDurations #'(4 . 5) {
            c'8 [ ( ~
            c'32
            d'16. ~
         }
         \time 1/20
         \scaleDurations #'(4 . 5) {
            d'16 ]
         }
         \time 2/8
         e'8 [
         f'8 ] )
   }'''

   assert check.wf(t)
   assert len(halves) == 2
   assert t.format == "\\new Staff {\n\t\t\\time 4/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'8 [ ( ~\n\t\t\tc'32\n\t\t\td'16. ~\n\t\t}\n\t\t\\time 1/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\td'16 ]\n\t\t}\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n}"
