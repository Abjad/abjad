from abjad.tools.pitchtools.list_named_pitches_in_expr import list_named_pitches_in_expr


def list_pitch_number_in_expr(expr):
   '''.. versionadded:: 1.1.2

   Get tuple or zero or more pitch numbers from almost any expression. ::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> pitchtools.list_pitch_number_in_expr(tuplet)
      (0, 2, 4)

   ::

      abjad> staff = Staff(macros.scale(4))
      abjad> pitchtools.list_pitch_number_in_expr(staff) 
      (0, 2, 4, 5)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_named_pitch_from_pitch_carrier_numbers( )`` to
      ``pitchtools.list_pitch_number_in_expr( )``.
   '''

   pitches = list_named_pitches_in_expr(expr)

   pitch_numbers = [pitch.pitch_number for pitch in pitches]
   pitch_numbers = tuple(pitch_numbers)

   return pitch_numbers
