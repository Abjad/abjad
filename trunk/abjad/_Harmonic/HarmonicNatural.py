from abjad._Harmonic.harmonic import _Harmonic
from abjad.Note import Note


class HarmonicNatural(Note, _Harmonic):
   '''Abjad model of natural string harmonics.'''

   def __init__(self, *args):
      Note.__init__(self, *args)
         
   ## OVERLOADS ##

   def __repr__(self):
      return 'HarmonicNatural(%s, %s)' % (self.pitch, self.duration)
