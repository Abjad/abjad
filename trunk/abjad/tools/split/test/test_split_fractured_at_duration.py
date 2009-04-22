from abjad import *


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
