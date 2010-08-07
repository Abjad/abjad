from abjad.tools.pitchtools.NumericPitchClass import NumericPitchClass


class NumericPitchClassColorMap(object):
   '''Color pitch-classes according to colors.'''

   def __init__(self, pitch_iterables, colors):
      assert len(pitch_iterables) == len(colors)
      self._pitch_iterables = pitch_iterables
      self._colors = colors
      self._init_color_dictionary( )

   ## OVERLOADS ##

   def __getitem__(self, pc):
      pc = NumericPitchClass(pc)
      color = self._color_dictionary[pc.number]
      return color

   def __repr__(self):
      sorted_keys = self._color_dictionary.keys( )
      sorted_keys.sort( )
      return '%s(%s)' % (self.__class__.__name__, sorted_keys)

   ## PRIVATE METHODS ##

   def _init_color_dictionary(self):
      self._color_dictionary = { }
      for pitch_iterable, color in zip(self.pitch_iterables, self.colors):
         for pitch in pitch_iterable:
            pc = NumericPitchClass(pitch)
            if pc.number in self._color_dictionary.keys( ):
               print pc, self._color_dictionary.keys( )
               raise KeyError(
                  'Duplicated pitch class %s in color dictionary.' % pc)
            self._color_dictionary[pc.number] = color

   ## PUBLIC ATTRIBUTES ##

   @property
   def colors(self):
      return self._colors

   @property
   def pairs(self):
      items = self._color_dictionary.items( )
      return list(sorted(items))

   @property
   def pitch_iterables(self):
      return self._pitch_iterables

   @property
   def twelve_tone_complete(self):
      pcs = range(12) 
      return set(pcs).issubset(set(self._color_dictionary.keys( )))

   @property
   def twenty_four_tone_complete(self):
      pcs = [x / 2.0 for x in range(24)]
      pcs = [int(x) if int(x) == x else x for x in pcs]
      return set(pcs).issubset(set(self._color_dictionary.keys( )))

   ## PUBLIC METHODS ##

   def get(self, key, alternative = None):
      try:
         return self[key]
      except (KeyError, TypeError, ValueError):
         return alternative
