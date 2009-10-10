from abjad.chord import Chord
from abjad.tools.pitchtools.PitchRange import PitchRange
from abjad.tools.pitchtools.PitchSet import PitchSet


## TODO: Reimplement pitchtools.octave_transpositions( ) as generator. ##

## TODO: Reimplement pitchtools.octave_transpositions( ) to work on Abjad PitchSet, Note and Chord objects only. ##

## TODO: Reimplement pitchtools.octave_transposition( ) with diatonic transposition. ##

def octave_transpositions(pitches, r):
#def octave_transpositions(chord, r):
   '''List all octave transpositions of `pitches` in range `r`.

   `pitches` may be an Abjad pitch-set or chord. `range` should
   be an Abjad PitchRange instance.

   ::

      abjad> pitchtools.octave_transpositions([0, 2, 4], [0, 48])
      [[0, 2, 4], [12, 14, 16], [24, 26, 28], [36, 38, 40]]

   ::
      
      abjad> chord = Chord([0, 2, 4], (1, 4))
      abjad> pitch_range = pitchtools.PitchRange(0, 48)
      abjad> pitchtools.octave_transpositions(chord, pitch_range)
   '''

   result = [ ]
   ps = set(pitches)
   R = set(range(r[0], r[-1] + 1))
   while ps.issubset(R):
      next = list(ps)
      next.sort( )
      result.extend([next])
      ps = set([p + 12 for p in ps])

   ps = set([p - 12 for p in pitches])
   while ps.issubset(R):
      next = list(ps)
      next.sort( )
      result.extend([next])
      ps = set([p - 12 for p in ps])

   result.sort( )
   return result

#   if not isinstance(chord, (Chord, PitchSet)):
#      raise TypeError('must be chord or pitch set.')
#
#   result = [ ]
#
#   interval = pitchtools.ChromaticInterval(0)
#   while True:
#      candidate = transpose_by_chromatic_interval(chord, interval)
#      if candidate in pitch_range:
#         result.append(candidate)
#         interval += pitchtools.ChromaticInterval(12) 
#      else:
#         break
#
#   interval = pitchtools.ChromaticInterval(-12)
#   while True:
#      candidate = transpose_by_chromatic_interval(chord, interval)
#      if candidate in pitch_range:
#         result.append(candidate)
#         interval -= pitchtools.ChromaticInterval(12) 
#      else:
#         break
#
#   return result
