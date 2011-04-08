from abjad.tools.pitchtools._Vector import _Vector


class NamedChromaticPitchVector(_Vector):
   '''.. versionadded:: 1.1.2

   Abjad model of named chromatic pitch vector::

      abjad> pitchtools.NamedChromaticPitchVector(["c''", "c''", "cs''", "cs''", "cs''"])
      NamedChromaticPitchVector(c'': 2, cs'': 3)

   Named chromatic pitch vectors are immutable.
   '''

   def __init__(self, pitch_tokens): 
      from abjad.tools import pitchtools
      for token in pitch_tokens:
         pitch = pitchtools.NamedChromaticPitch(token)
         try:
            dict.__setitem__(self, str(pitch), self[str(pitch)] + 1)
         except KeyError:
            dict.__setitem__(self, str(pitch), 1)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      pitches = self.pitches
      if not pitches:
         return ' '
      substrings = [ ]
      for pitch in pitches:
         count = self[str(pitch)]
         substring = '%s: %s' % (pitch, count)
         substrings.append(substring)
      return ', '.join(substrings)

   ## PUBLIC ATTRIBUTES ##

   @property
   def numbers(self):
      numbers = [ ]
      for pitch in self.pitches:
         number = pitch.number
         if number not in numbers:
            numbers.append(number)
      numbers.sort( )
      return numbers

   @property
   def pitches(self):
      from abjad.tools import pitchtools
      pitches = [pitchtools.NamedChromaticPitch(key) for key, value in self.items( )]
      pitches.sort( )
      return pitches
