from abjad.components._Harmonic._Harmonic import _Harmonic
from abjad.components.Note import Note


class NaturalHarmonic(Note, _Harmonic):
   '''Abjad model of natural string harmonics.'''

   def __init__(self, *args):
      Note.__init__(self, *args)
         
   ## OVERLOADS ##

   def __repr__(self):
      return 'NaturalHarmonic(%s, %s)' % (self.pitch, self.duration)
