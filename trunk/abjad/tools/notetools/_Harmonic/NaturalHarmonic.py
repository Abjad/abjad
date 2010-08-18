from abjad.components._Harmonic._Harmonic import _Harmonic
from abjad.components.Note import Note


class NaturalHarmonic(Note, _Harmonic):
   '''Abjad model of natural string harmonics.'''

   def __init__(self, *args):
      Note.__init__(self, *args)
      self.override.note_head.style = 'harmonic'
         
   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self.pitch, self.duration)
