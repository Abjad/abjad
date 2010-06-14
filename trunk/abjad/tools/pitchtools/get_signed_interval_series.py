from abjad.tools import listtools
from abjad.tools.pitchtools.get_pitch import get_pitch
from abjad.tools.pitchtools.is_carrier import is_carrier


def get_signed_interval_series(pitch_carriers, wrap = False):
   r'''Return list of signed integers representing the intervals
   between each of the elements in *pitch_carriers*.
   
   Behavior of ``wrap``:

   *  When ``wrap = False`` do not return \
      ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.
   *  When ``wrap = True`` do return \
      ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.
   *  Default to ``False``.

   ::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))
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

      abjad> pitchtools.get_signed_interval_series(t)
      [2, 2, 1, 2, 2, 2, 1]

   ::

      abjad> pitchtools.get_signed_interval_series(t, wrap = True)
      [2, 2, 1, 2, 2, 2, 1, -12]

   ::

      abjad> notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(8)  
      abjad> notes.reverse( )
      abjad> notes
      [Note(c'', 8), Note(b', 8), Note(a', 8), Note(g', 8), Note(f', 8), Note(e', 8), Note(d', 8), Note(c', 8)]

   ::

      abjad> pitchtools.get_signed_interval_series(notes)
      [-1, -2, -2, -2, -1, -2, -2]

   ::

      abjad> pitchtools.get_signed_interval_series(notes, wrap = True)
      [-1, -2, -2, -2, -1, -2, -2, 12]
   '''

   result = [ ]

   if len(pitch_carriers) == 0:
      return result
   elif len(pitch_carriers) == 1:
      if is_carrier(pitch_carriers[0]):
         return result
      else:
         raise TypeError('must be Abjad Pitch, Note, NoteHead or Chord.')

   if wrap:
      pairs = listtools.pairwise(pitch_carriers, mode = 'wrap')
   else:
      pairs = listtools.pairwise(pitch_carriers)

   for first_carrier, second_carrier in pairs:
      first_pitch = get_pitch(first_carrier)
      second_pitch = get_pitch(second_carrier)
      signed_interval = second_pitch.number - first_pitch.number
      result.append(signed_interval)

   return result
