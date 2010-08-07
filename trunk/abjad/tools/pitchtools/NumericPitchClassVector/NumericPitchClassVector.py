from abjad.tools.pitchtools.NumericPitchClass import NumericPitchClass


class NumericPitchClassVector(dict):
   '''.. versionadded:: 1.1.2

   Tallies by pitch class.
   '''

   def __init__(self, pitch_class_tokens):
      for pcn in range(12):
         self[pcn] = 0
         self[pcn + 0.5] = 0
      for token in pitch_class_tokens:
         pitch_class = NumericPitchClass(token)
         self[pitch_class.number] += 1

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      string = self._twelve_tone_format_string
      if self._has_quartertones:
         string += '\n%s' % self._quartertone_format_string
      return string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _first_quartertone_sextet_string(self):
      items = self._quartertone_items[:6]
      substrings = [ ]
      for pitch_class_number, count in sorted(items):
         substring = '%s' % count
         substrings.append(substring)
      return ' '.join(substrings)

   @property
   def _first_twelve_tone_sextet_string(self):
      items = self._twelve_tone_items[:6]
      substrings = [ ]
      for pitch_class_number, count in sorted(items):
         substring = '%s' % count
         substrings.append(substring)
      return ' '.join(substrings)

   @property
   def _format_string(self):
      string = self._twelve_tone_format_string
      if self._has_quartertones:
         string += ' || %s' % self._quartertone_format_string
      return string

   @property
   def _has_quartertones(self):
      return any([0 < item[1] for item in self._quartertone_items])

   @property
   def _quartertone_format_string(self):
      return '%s | %s' % (
         self._first_quartertone_sextet_string, 
         self._second_quartertone_sextet_string)

   @property
   def _quartertone_items(self):
      items = [item for item in self.items( ) if isinstance(item[0], float)]
      items.sort( )
      return items

   @property
   def _second_quartertone_sextet_string(self):
      items = self._quartertone_items[6:]
      substrings = [ ]
      for pitch_class_number, count in sorted(items):
         substring = '%s' % count
         substrings.append(substring)
      return ' '.join(substrings)
      
   @property
   def _second_twelve_tone_sextet_string(self):
      items = self._twelve_tone_items[6:]
      substrings = [ ]
      for pitch_class_number, count in sorted(items):
         substring = '%s' % count
         substrings.append(substring)
      return ' '.join(substrings)
      
   @property
   def _twelve_tone_format_string(self):
      return '%s | %s' % (
         self._first_twelve_tone_sextet_string, 
         self._second_twelve_tone_sextet_string)

   @property
   def _twelve_tone_items(self):
      items = [item for item in self.items( ) if isinstance(item[0], int)]
      items.sort( )
      return items

   ## PUBLIC ATTRIBUTES ##

   @property
   def numbers(self):
      numbers = [pitch_class.number for pitch_class in self.pitch_classes]
      numbers.sort( )
      return numbers

   @property
   def pitch_classes(self):
      pitch_classes = [ ]
      for pitch_class_number, count in self.items( ):
         if 0 < count:
            pitch_class = NumericPitchClass(pitch_class_number)
            pitch_classes.append(pitch_class)
      return pitch_classes
