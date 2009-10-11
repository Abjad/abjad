from abjad.chord import Chord
from abjad.tools.pitchtools.ChromaticInterval import ChromaticInterval
from abjad.tools.pitchtools.PitchRange import PitchRange
from abjad.tools.pitchtools.PitchSet import PitchSet
from abjad.tools.pitchtools.transpose_by_chromatic_interval import \
   transpose_by_chromatic_interval


## TODO: Reimplement pitchtools.octave_transpositions( ) to work on Abjad PitchSet, Note and Chord objects only. ##

## TODO: Reimplement pitchtools.octave_transposition( ) with diatonic transposition. ##

#def octave_transpositions(pitches, r):
def octave_transpositions(chord, pitch_range):
   r"""List all octave transpositions of `pitches` in range `r`.

   `pitches` may be an Abjad pitch-set or chord. `pitch_range` should
   be an Abjad PitchRange instance.

   ::
      
      abjad> chord = Chord([0, 2, 4], (1, 4))
      abjad> pitch_range = pitchtools.PitchRange(0, 48)
      abjad> pitchtools.octave_transpositions(chord, pitch_range)
      [Chord(c' d' e', 4), Chord(c'' d'' e'', 4), Chord(c''' d''' e''', 4), Chord(c'''' d'''' e'''', 4)]
   """

   if not isinstance(pitch_range, PitchRange):
      raise TypeError('must be pitch range.')

   if all([isinstance(x, (int, long, float)) for x in chord]):
      return _pitch_number_list_octave_transpositions(chord, pitch_range)

   if not isinstance(chord, (Chord, PitchSet)):
      raise TypeError('must be chord or pitch set.')

   result = [ ]

   interval = ChromaticInterval(-12)
   while True:
      candidate = transpose_by_chromatic_interval(chord, interval)
      if candidate in pitch_range:
         result.append(candidate)
         interval -= ChromaticInterval(12) 
      else:
         break

   result.reverse( )

   interval = ChromaticInterval(0)
   while True:
      candidate = transpose_by_chromatic_interval(chord, interval)
      if candidate in pitch_range:
         result.append(candidate)
         interval += ChromaticInterval(12) 
      else:
         break

   return result


def _pitch_number_list_octave_transpositions(pitch_number_list, pitch_range):
   result = [ ]
   ps = set(pitch_number_list)
   start_pitch_number = pitch_range._start_pitch.number
   stop_pitch_number = pitch_range._stop_pitch.number
   R = set(range(start_pitch_number, stop_pitch_number + 1))
   while ps.issubset(R):
      next = list(ps)
      next.sort( )
      result.extend([next])
      ps = set([p + 12 for p in ps])

   ps = set([p - 12 for p in pitch_number_list])
   while ps.issubset(R):
      next = list(ps)
      next.sort( )
      result.extend([next])
      ps = set([p - 12 for p in ps])

   result.sort( )
   return result
