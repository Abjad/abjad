from abjad.tools.pitchtools.PitchRange import PitchRange


## TODO: Reimplement pitchtools.octave_transpositions( ) as generator. ##
## TODO: Reimplement pitchtools.octave_transpositions( ) to work on Abjad PitchSet, Note and Chord objects only. ##

def octave_transpositions(pitches, r):
   '''List all octave transpositions of `pitches` in range `r`.

   ::

      abjad> pitchtools.octave_transpositions([0, 2, 4], [0, 48])
      [[0, 2, 4], [12, 14, 16], [24, 26, 28], [36, 38, 40]]
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
