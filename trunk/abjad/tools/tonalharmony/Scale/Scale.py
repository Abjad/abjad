from abjad.tools.pitchtools.NamedPitchClass import NamedPitchClass
import copy


class Scale(list):
   '''.. versionadded:: 1.1.2

   Ordered collection of named pitch-class instances.
   '''

   def __init__(self, key_signature):
      if not isinstance(key_signature, KeySignature):
         raise TypeError('%s is not key signature instance.' % key_signature)
      npcs = self._key_signature_to_named_pitch_classes(key_signature)
      self.extend(npcs)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '<%s>' % self._format_string
      
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   ## PRIVATE METHODS ##

   def _key_signature_to_npcs(self, key_signature):
      if key_signature == KeySignature('c', 'major'):
         names = ('c', 'd', 'e', 'f', 'g', 'a', 'b')
      elif key_signature == KeySignature('d', 'major'):
         names = ('d', 'e', 'fs', 'g', 'a', 'b', 'cs')


   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class_segment(self):
      interval_classes = list(listtools.difference_series(self.pitch_classes))
      return IntervalClassSegment(interval_classes)

   @property
   def pitch_class_set(self):
      return PitchClassSet(self)

   @property
   def pitch_classes(self):
      return tuple(self[:])

   ## PUBLIC METHODS ##

   def invert(self):
      return PitchClassSegment([pc.invert( ) for pc in self])
      
   def multiply(self, n):
      return PitchClassSegment([pc.multiply(n) for pc in self])

   def retrograde(self):
      return PitchClassSegment(reversed(self))

   def rotate(self, n):
      from abjad.tools import listtools
      pitch_classes = listtools.rotate(self.pitch_classes, n)
      return PitchClassSegment(pitch_classes)
      
   def transpose(self, n):
      return PitchClassSegment([pc.transpose(n) for pc in self])
