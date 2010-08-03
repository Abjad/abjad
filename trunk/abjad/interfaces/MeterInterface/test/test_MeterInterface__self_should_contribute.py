from abjad import *


def test_MeterInterface__self_should_contribute_01( ):
   r'''In this real-world, nested structure, 
      components at all four levels of the score tree neither
      can nor should conribute LilyPond \time indication at format-time.

      The exception is the measure, which both can and should
      contribute LilyPond \time indication at format-time.'''

   notes = macros.scale(3)
   tuplet = FixedDurationTuplet((2, 8), notes)
   measure = RigidMeasure((2, 8), [tuplet])
   staff = Staff([measure])

   r'''
   \new Staff {
         \time 2/8
         \times 2/3 {
            c'8
            d'8
            e'8
         }
   }
   '''

   assert not notes[0].meter._self_can_contribute
   assert not notes[0].meter._self_should_contribute

   assert not tuplet.meter._self_can_contribute
   assert not tuplet.meter._self_should_contribute

   assert measure.meter._self_can_contribute
   assert measure.meter._self_should_contribute

   assert not staff.meter._self_can_contribute
   assert not staff.meter._self_should_contribute


def test_MeterInterface__self_should_contribute_02( ):
   r'''Orphan note both can and should contribute LilyPond \time
      indication at format-time.'''

   t = Note(0, (1, 4))
   t.meter.forced = Meter(1, 4)

   r'''
   \time 1/4
   c'4
   '''

   assert t.meter._self_can_contribute
   assert t.meter._self_should_contribute


def test_MeterInterface__self_should_contribute_03( ):
   r'''Here we force meter on the parented note.
      The note now both can and should contribute LilyPond \time.
      The parent tuplet neither can nor should contribute LilyPond \time.'''

   t = FixedDurationTuplet((2, 8), macros.scale(3))
   t[0].meter.forced = Meter(2, 8)

   r'''
   \times 2/3 {
      \time 2/8
      c'8
      d'8
      e'8
   }
   '''

   assert t[0].meter._self_can_contribute
   assert t[0].meter._self_should_contribute

   assert not t.meter._self_can_contribute
   assert not t.meter._self_should_contribute


def test_MeterInterface__self_should_contribute_04( ):
   r'''Here we force meter on the parent tuplet.
      The note neither can nor should contribute LilyPond \time.
      The parent tuplet both can and should contribute LilyPond \time.'''

   t = FixedDurationTuplet((2, 8), macros.scale(3))
   t.meter.forced = Meter(2, 8)

   r'''
   \times 2/3 {
      \time 2/8
      c'8
      d'8
      e'8
   }
   '''

   assert not t[0].meter._self_can_contribute
   assert not t[0].meter._self_should_contribute

   assert t.meter._self_can_contribute
   assert t.meter._self_should_contribute
