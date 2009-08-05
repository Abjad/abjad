from abjad import *


def test_partition_cyclic_fractured_by_durations_01( ):
   '''Cyclically duration partition one leaf in score.
      Fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

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

   durations = [Rational(3, 64)]
   parts = partition.cyclic_fractured_by_durations(t[0][1:2], durations)

   r'''
   \new Staff {
      {
         \time 2/8
         c'8 [ (
         d'32. )
         d'32. ( )
         d'64 ( ~
         d'64 ]
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32. )\n\t\td'32. ( )\n\t\td'64 ( ~\n\t\td'64 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_partition_cyclic_fractured_by_durations_02( ):
   '''Cyclically duration partition multiple leaves in score.
      Fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

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

   durations = [Rational(3, 32)]
   parts = partition.cyclic_fractured_by_durations(t.leaves, durations)

   r'''
   \new Staff {
      {
         \time 2/8
         c'16. ( ) [
         c'32 (
         d'16 )
         d'16 ] (
      }
      {
         \time 2/8
         e'32 ) [
         e'16. (
         f'16. )
         f'32 ] ( )
      }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 6
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16. ( ) [\n\t\tc'32 (\n\t\td'16 )\n\t\td'16 ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'32 ) [\n\t\te'16. (\n\t\tf'16. )\n\t\tf'32 ] ( )\n\t}\n}"


def test_partition_cyclic_fractured_by_durations_03( ):
   '''Cyclically duration partition one measure in score.
      Fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

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

   durations = [Rational(3, 32)]
   parts = partition.cyclic_fractured_by_durations(t[:1], durations)

   r'''
   \new Staff {
      {
         \time 3/32
         c'16. [ ] ( )
      }
      {
         \time 3/32
         c'32 [ (
         d'16 ] )
      }
      {
         \time 2/32
         d'16 [ ] (
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 3
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'32 [ (\n\t\td'16 ] )\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_partition_cyclic_fractured_by_durations_04( ):
   '''Cyclically duration partition multiple measures in score.
      Fracture spanners.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

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

   durations = [Rational(3, 32)]
   parts = partition.cyclic_fractured_by_durations(t[:], durations)

   r'''
   \new Staff {
      {
         \time 3/32
         c'16. [ ] ( )
      }
      {
         \time 3/32
         c'32 [ (
         d'16 ] )
      }
      {
         \time 2/32
         d'16 [ ] (
      }
      {
         \time 1/32
         e'32 [ ] )
      }
      {
         \time 3/32
         e'16. [ ] ( )
      }
      {
         \time 3/32
         f'16. [ ] ( )
      }
      {
         \time 1/32
         f'32 [ ] ( )
      }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 6
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'32 [ (\n\t\td'16 ] )\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] )\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tf'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ] ( )\n\t}\n}"


def test_partition_cyclic_fractured_by_durations_05( ):
   '''Cyclically duration partition list of leaves outside of score.'''

   leaves = construct.scale(4)
   durations = [Rational(3, 32)]
   parts = partition.cyclic_fractured_by_durations(leaves, durations)

   assert len(parts) == 6

   t = Staff([ ])
   for part in parts:
      t.extend(part)

   r'''\new Staff {
           c'16.
           c'32
           d'16
           d'16
           e'32
           e'16.
           f'16.
           f'32
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'16.\n\tc'32\n\td'16\n\td'16\n\te'32\n\te'16.\n\tf'16.\n\tf'32\n}"


def test_partition_cyclic_fractured_by_durations_06( ):
   '''Cyclically duration partition list of measures outside of score.
      Fracture spanners.'''

   measures = RigidMeasure((2, 8), construct.run(2)) * 2
   Beam(measures[0])
   Beam(measures[1])
   pitchtools.diatonicize(measures)

   durations = [Rational(3, 32)]
   parts = partition.cyclic_fractured_by_durations(measures, durations)

   assert len(parts) == 6

   t = Staff([ ])
   for part in parts:
      t.extend(part)

   r'''
   \new Staff {
      {
         \time 3/32
         c'16. [ ]
      }
      {
         \time 3/32
         c'32 [
         d'16 ]
      }
      {
         \time 2/32
         d'16 [ ]
      }
      {
         \time 1/32
         e'32 [ ]
      }
      {
         \time 3/32
         e'16. [ ]
      }
      {
         \time 3/32
         f'16. [ ]
      }
      {
         \time 1/32
         f'32 [ ]
      }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ]\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'32 [\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ]\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ]\n\t}\n\t{\n\t\t\\time 3/32\n\t\tf'16. [ ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ]\n\t}\n}"


def test_partition_cyclic_fractured_by_durations_07( ):
   '''Duration partition one leaf in score.
      Read durations cyclically in list.
      Fracture spanners but add tie after each split.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

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

   durations = [Rational(1, 32)]
   parts = partition.cyclic_fractured_by_durations(
      t[0][1:], durations, tie_after = True)

   r'''
   \new Staff {
      {
         \time 2/8
         c'8 [ (
         d'32 ) ~
         d'32 ( ) ~
         d'32 ( ) ~
         d'32 ] (
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 4
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32 ) ~\n\t\td'32 ( ) ~\n\t\td'32 ( ) ~\n\t\td'32 ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"



def test_partition_cyclic_fractured_by_durations_08( ):
   '''Duration partition multiple leaves in score.
      Read durations cyclically in list.
      Fracture spanners but add tie after each split.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

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

   durations = [Rational(1, 16)]
   parts = partition.cyclic_fractured_by_durations(
      t.leaves, durations, tie_after = True)

   r'''
   \new Staff {
      {
         \time 2/8
         c'16 ( ) [ ~
         c'16 (
         d'16 ) ~
         d'16 ] (
      }
      {
         \time 2/8
         e'16 ) [ ~
         e'16 (
         f'16 ) ~
         f'16 ] ( )
      }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 8
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16 ( ) [ ~\n\t\tc'16 (\n\t\td'16 ) ~\n\t\td'16 ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'16 ) [ ~\n\t\te'16 (\n\t\tf'16 ) ~\n\t\tf'16 ] ( )\n\t}\n}"


def test_partition_cyclic_fractured_by_durations_09( ):
   '''Duration partition one measure in score.
      Read durations cyclically in list.
      Fracture spanners but add tie after each split.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

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

   durations = [Rational(1, 16)]
   parts = partition.cyclic_fractured_by_durations(
      t[:1], durations, tie_after = True)

   r'''
   \new Staff {
      {
         \time 1/16
         c'16 [ ] ( ) ~
      }
      {
         \time 1/16
         c'16 [ ] ( )
      }
      {
         \time 1/16
         d'16 [ ] ( ) ~
      }
      {
         \time 1/16
         d'16 [ ] (
      }
      {
         \time 2/8
         e'8 [
         f'8 ] )
      }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 4
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\tc'16 [ ] ( ) ~\n\t}\n\t{\n\t\t\\time 1/16\n\t\tc'16 [ ] ( )\n\t}\n\t{\n\t\t\\time 1/16\n\t\td'16 [ ] ( ) ~\n\t}\n\t{\n\t\t\\time 1/16\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"



def test_partition_cyclic_fractured_by_durations_10( ):
   '''Duration partition multiple measures in score.
      Read durations cyclically in list.
      Fracture spanners but add tie after each split.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

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

   durations = [Rational(3, 32)]
   parts = partition.cyclic_fractured_by_durations(
      t[:], durations, tie_after = True)

   r'''
   \new Staff {
      {
         \time 3/32
         c'16. [ ] ( ) ~
      }
      {
         \time 3/32
         c'32 [ (
         d'16 ] ) ~
      }
      {
         \time 2/32
         d'16 [ ] (
      }
      {
         \time 1/32
         e'32 [ ] ) ~
      }
      {
         \time 3/32
         e'16. [ ] ( )
      }
      {
         \time 3/32
         f'16. [ ] ( ) ~
      }
      {
         \time 1/32
         f'32 [ ] ( )
      }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 6
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( ) ~\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'32 [ (\n\t\td'16 ] ) ~\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] ) ~\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tf'16. [ ] ( ) ~\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ] ( )\n\t}\n}"
