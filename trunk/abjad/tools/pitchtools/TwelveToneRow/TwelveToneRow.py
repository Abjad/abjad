from abjad.tools.pitchtools.NumericPitchClass import NumericPitchClass


class TwelveToneRow(object):
   '''.. versionadded:: 1.1.2

   '''

   def __init__(self, pitch_classes):
      pitch_classes = [NumericPitchClass(pc) for pc in pitch_classes]
      self._validate_pitch_classes(pitch_classes)
      self._pitch_classes = pitch_classes

   ## OVERLOADS ##

   def __contains__(self, arg):
      return arg in self.pitch_classes

   def __copy__(self):
      return TwelveToneRow(self)

   def __eq__(self, arg):
      if isinstance(arg, TwelveToneRow):
         return self.pitch_classes == arg.pitch_classes
      return False

   def __getitem__(self, arg):
      if isinstance(arg, int):
         return self.pitch_classes[arg]
      elif isinstance(arg, slice):
         start, stop, step = arg.indices(len(self))
         result = [ ]
         for i in range(start, stop, step):
            result.append(self[i])
         return tuple(result)
      else:
         raise ValueError('must be integer or slice.')

   def __len__(self):
      return len(self.pitch_classes)

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._contents_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_string(self):
      return ', '.join([str(pc.number) for pc in self.pitch_classes])

   ## PRIVATE METHODS ##

   def _validate_pitch_classes(self, pitch_classes):
      numbers = [pc.number for pc in pitch_classes]
      numbers.sort( )
      if not numbers == range(12):
         raise ValueError('must contain all twelve pitch classes.')

   ## PUBLIC ATTRIBUTES ##

   @property
   def pitch_classes(self):
      '''Read-only tuple of pitch-classes in row.'''
      return tuple(self._pitch_classes)

   ## PUBLIC METHODS ##

   def alpha(self):
      numbers = [ ]
      for pc in self.pitch_classes:
         if pc.number % 2 == 0:
            numbers.append((pc.number + 1) % 12)
         else:
            numbers.append(pc.number - 1)
      return TwelveToneRow(numbers)

   def invert(self):
      numbers = [12 - pc.number for pc in self.pitch_classes]
      return TwelveToneRow(numbers)

   def reverse(self):
      return TwelveToneRow(reversed(self.pitch_classes))

   def transpose(self, n):
      if not isinstance(n, int):
         raise TypeError
      numbers = [(pc.number + n) % 12 for pc in self.pitch_classes]
      return TwelveToneRow(numbers)
