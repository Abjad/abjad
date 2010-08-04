from abjad.NamedPitch import NamedPitch


class PitchVector(dict):
   '''.. versionadded:: 1.1.2

   Tallies by pitch.
   '''

   def __init__(self, pitch_tokens): 
      for token in pitch_tokens:
         pitch = NamedPitch(token)
         try:
            self[pitch.pair] += 1
         except KeyError:
            self[pitch.pair] = 1

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
         count = self[pitch.pair]
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
      pitches = [NamedPitch(key) for key, value in self.items( )]
      pitches.sort( )
      return pitches
