from abjad import *


def test_partition_unfractured_by_durations_01( ):
   '''Duration partition one container in score
      Do no fracture spanners.'''

   t = Staff(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''
   \new Staff {
      {
         c'8 [ (
         d'8 ]
      }
      {
         e'8 [
         f'8 ] )
      }
   }
   '''

   durations = [Rational(1, 32), Rational(3, 32), Rational(5, 32)]
   parts = partition.unfractured_by_durations(t[:1], durations)

   r'''
   \new Staff {
      {
         c'32 [ (
      }
      {
         c'16.
      }
      {
         d'8 ]
      }
      {
         e'8 [
         f'8 ] )
      }
   }
   '''


   assert check.wf(t)
   assert len(parts) == 3
   assert t.format == "\\new Staff {\n\t{\n\t\tc'32 [ (\n\t}\n\t{\n\t\tc'16.\n\t}\n\t{\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_partition_unfractured_by_durations_02( ):
   '''Duration partition multiple containers in score.
      Do not fracture spanners.'''

   t = Staff(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Slur(t.leaves)

   r'''
   \new Staff {
      {
         c'8 [ (
         d'8 ]
      }
      {
         e'8 [
         f'8 ] )
      }
   }
   '''

   durations = [Rational(1, 32), Rational(3, 32), Rational(5, 32)]
   parts = partition.unfractured_by_durations(t[:], durations)

   r'''
   \new Staff {
      {
         c'32 [ (
      }
      {
         c'16.
      }
      {
         d'8 ]
      }
      {
         e'32 [
      }
      {
         e'16.
         f'8 ] )
      }
   }
   '''

   assert check.wf(t)
   assert len(parts) == 4
   assert t.format == "\\new Staff {\n\t{\n\t\tc'32 [ (\n\t}\n\t{\n\t\tc'16.\n\t}\n\t{\n\t\td'8 ]\n\t}\n\t{\n\t\te'32 [\n\t}\n\t{\n\t\te'16.\n\t\tf'8 ] )\n\t}\n}"
