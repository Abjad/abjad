from abjad.tools import listtools
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import \
   get_named_chromatic_pitch_from_pitch_carrier
from abjad.tools.pitchtools.is_pitch_carrier import is_pitch_carrier


def list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(
   pitch_carriers, wrap = False):
   r'''Return list of signed integers representing the intervals
   between each of the elements in *pitch_carriers*.
   
   Behavior of ``wrap``:

   *  When ``wrap = False`` do not return
      ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.
   *  When ``wrap = True`` do return
      ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.
   *  Default to ``False``.

   ::

      abjad> staff = Staff(macros.scale(8))
      abjad> print staff.format
      \new Staff {
              c'8
              d'8
              e'8
              f'8
              g'8
              a'8
              b'8
              c''8
      }

   ::

      abjad> pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(t)
      [2, 2, 1, 2, 2, 2, 1]

   ::

      abjad> pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(t, wrap = True)
      [2, 2, 1, 2, 2, 2, 1, -12]

   ::

      abjad> notes = macros.scale(8)  
      abjad> notes.reverse( )
      abjad> notes
      [Note(c'', 8), Note(b', 8), Note(a', 8), Note(g', 8), Note(f', 8), Note(e', 8), Note(d', 8), Note(c', 8)]

   ::

      abjad> pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(notes)
      [-1, -2, -2, -2, -1, -2, -2]

   ::

      abjad> pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(notes, wrap = True)
      [-1, -2, -2, -2, -1, -2, -2, 12]

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_signed_interval_series( )`` to
      ``pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_pitches( )`` to
      ``pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers( )``.
   '''

   result = [ ]

   if len(pitch_carriers) == 0:
      return result
   elif len(pitch_carriers) == 1:
      if is_pitch_carrier(pitch_carriers[0]):
         return result
      else:
         raise TypeError('must be Abjad Pitch, Note, NoteHead or Chord.')

   if wrap:
      pairs = listtools.pairwise(pitch_carriers, mode = 'wrap')
   else:
      pairs = listtools.pairwise(pitch_carriers)

   for first_carrier, second_carrier in pairs:
      first_pitch = get_named_chromatic_pitch_from_pitch_carrier(first_carrier)
      second_pitch = get_named_chromatic_pitch_from_pitch_carrier(second_carrier)
      signed_interval = second_pitch.pitch_number - first_pitch.pitch_number
      result.append(signed_interval)

   return result
