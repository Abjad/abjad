from abjad import *


def test_partition_fractured_by_durations_01( ):
   '''Duration partition one container in score, and fracture spanners.'''

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

   durations = [Rational(1, 32), Rational(3, 32), Rational(5, 32)]
   parts = partition.fractured_by_durations(t[:1], durations)

   r'''
   \new Staff {
           {
                   \time 1/32
                   c'32 [ ] ( )
           }
           {
                   \time 3/32
                   c'16. [ ] ( )
           }
           {
                   \time 4/32
                   d'8 [ ] (
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
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_partition_fractured_by_durations_02( ):
   '''Duration partition multiple containers in score, 
      and fracture spanners.'''

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

   durations = [Rational(1, 32), Rational(3, 32), Rational(5, 32)]
   parts = partition.fractured_by_durations(t[:], durations)

   r'''
   \new Staff {
           {
                   \time 1/32
                   c'32 [ ] ( )
           }
           {
                   \time 3/32
                   c'16. [ ] ( )
           }
           {
                   \time 4/32
                   d'8 [ ] (
           }
           {
                   \time 1/32
                   e'32 [ ] )
           }
           {
                   \time 7/32
                   e'16. [ (
                   f'8 ] )
           }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 4
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] )\n\t}\n\t{\n\t\t\\time 7/32\n\t\te'16. [ (\n\t\tf'8 ] )\n\t}\n}"


def test_partition_fractured_by_durations_03( ):
   '''Duration partition container outside of score.
      This example includes no spanners.
      Spanners do not apply outside of score.'''

   t = Container(construct.run(2)) * 2
   pitchtools.diatonicize(t)

   "[{c'8, d'8}, {e'8, f'8}]"

   durations = [Rational(1, 32), Rational(3, 32), Rational(5, 32)]
   parts = partition.fractured_by_durations(t, durations)

   "[[{c'32}], [{c'16.}], [{d'8}, {e'32}], [{e'16., f'8}]]"

   assert len(parts) == 4


def test_partition_fractured_by_durations_04( ):
   '''Duration partition one leaf outside of score.'''

   t = Note(0, (1, 4))

   "c'4"

   durations = [Rational(1, 32), Rational(5, 32)]
   parts = partition.fractured_by_durations([t], durations)

   "[[Note(c', 32)], [Note(c', 8), Note(c', 32)], [Note(c', 16)]]"

   assert len(parts) == 3


def test_partition_fractured_by_durations_05( ):
   '''Duration partition leaf in score and fracture spanners.'''

   t = Staff([Note(0, (1, 8))])
   Beam(t[0])

   r'''\new Staff {
      c'8 [ ]
   }'''

   durations = [Rational(1, 64), Rational(5, 64)]
   parts = partition.fractured_by_durations(t[:], durations)

   r'''\new Staff {
      c'64 [ ]
      c'16 [ ~
      c'64 ]
      c'32 [ ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'64 [ ]\n\tc'16 [ ~\n\tc'64 ]\n\tc'32 [ ]\n}"
