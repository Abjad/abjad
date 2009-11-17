from abjad.tools.pitchtools.get_pitches import get_pitches


def get_pitch_numbers(expr):
   '''.. versionadded:: 1.1.2

   Get tuple or zero or more pitch numbers from almost any expression. ::

      abjad> tuplet = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> pitchtools.get_pitch_numbers(tuplet)
      (0, 2, 4)

   ::

      abjad> staff = Staff(construct.scale(4))
      abjad> pitchtools.get_pitch_numbers(staff) 
      (0, 2, 4, 5)
   '''

   pitches = get_pitches(expr)

   pitch_numbers = [pitch.number for pitch in pitches]
   pitch_numbers = tuple(pitch_numbers)

   return pitch_numbers
