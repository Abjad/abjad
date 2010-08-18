from abjad.core import Rational
from abjad.components._Tuplet.FixedMultiplierTuplet._FixedMultiplierTupletDurationInterface import \
   _FixedMultiplierTupletDurationInterface
from abjad.components._Tuplet._Tuplet import _Tuplet


class Tuplet(_Tuplet):
   '''Abjad model of tuplet with fixed multiplier.'''

   def __init__(self, multiplier, music = None, **kwargs):
      '''Init fixed-multiplier tuplet as type of Abjad tuplet.'''
      _Tuplet.__init__(self, music)
      self._duration = _FixedMultiplierTupletDurationInterface(self, multiplier)
      self._signifier = '*'
      self._initialize_keyword_values(**kwargs)

   ## REPR ##

   def __repr__(self):
      return '%s(%s, [%s])' % ( 
         self.__class__.__name__, self.duration.multiplier, self._summary)

   def __str__(self):
      if 0 < len(self):
         return '{%s %s %s %s}' % (self._signifier, self.ratio, self._summary, self._signifier)
      else:
         return '{%s %s %s}' % (self._signifier, self.duration.multiplier, self._signifier)

   ## PROPERTIES ##

   @property
   def duration(self):
      ''':class:`~abjad.components._Tuplet.FixedMultiplierTuplet._FixedMultiplierTupletDurationInterface` \
      duration interface.'''
      return self._duration
