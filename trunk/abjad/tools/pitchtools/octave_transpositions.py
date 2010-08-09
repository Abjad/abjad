from abjad.components.Chord import Chord
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.PitchRange import PitchRange
from abjad.tools.pitchtools.NamedPitchSet import NamedPitchSet
from abjad.tools.pitchtools.transpose_by_melodic_chromatic_interval import transpose_by_melodic_chromatic_interval


## TODO: Reimplement pitchtools.octave_transpositions( ) to work on Abjad PitchSet, Note and Chord objects only. ##

## TODO: Reimplement pitchtools.octave_transposition( ) with diatonic transposition. ##

def octave_transpositions(pitches, pitch_range):
   r"""List octave transpositions of `pitches` in `pitch_range`.

   ::
      
      abjad> chord = Chord([0, 2, 4], (1, 4))
      abjad> pitch_range = pitchtools.PitchRange(0, 48)
      abjad> pitchtools.octave_transpositions(chord, pitch_range)
      [Chord(c' d' e', 4), Chord(c'' d'' e'', 4), Chord(c''' d''' e''', 4), Chord(c'''' d'''' e'''', 4)]
   """

   if not isinstance(pitch_range, PitchRange):
      raise TypeError('must be pitch range.')

   if all([isinstance(x, (int, long, float)) for x in pitches]):
      return _pitch_number_list_octave_transpositions(pitches, pitch_range)

   if not isinstance(pitches, (Chord, NamedPitchSet)):
      raise TypeError('must be pitches or pitch set.')

   result = [ ]

   interval = MelodicChromaticInterval(-12)
   while True:
      candidate = transpose_by_melodic_chromatic_interval(pitches, interval)
      if candidate in pitch_range:
         result.append(candidate)
         interval -= MelodicChromaticInterval(12) 
      else:
         break

   result.reverse( )

   interval = MelodicChromaticInterval(0)
   while True:
      candidate = transpose_by_melodic_chromatic_interval(pitches, interval)
      if candidate in pitch_range:
         result.append(candidate)
         interval += MelodicChromaticInterval(12) 
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
