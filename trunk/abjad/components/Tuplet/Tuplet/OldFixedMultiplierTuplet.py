from abjad.core import Rational
from abjad.components.Tuplet._Tuplet import _Tuplet


class OldFixedMultiplierTuplet(_Tuplet):
   '''Abjad model of tuplet with fixed multiplier.'''

#   def __init__(self, multiplier, music = None, **kwargs):
#      '''Init fixed-multiplier tuplet as type of Abjad tuplet.'''
#      _Tuplet.__init__(self, multiplier, music)
#      self._signifier = '*'
#      self._initialize_keyword_values(**kwargs)
#
#   ## REPR ##
#
#   def __repr__(self):
#      #return '%s(%s, [%s])' % ( 
#      #   self.__class__.__name__, self.duration.multiplier, self._summary)
#      return '%s(%s, [%s])' % ( 
#         'Tuplet', self.duration.multiplier, self._summary)
#
#   def __str__(self):
#      if 0 < len(self):
#         return '{%s %s %s %s}' % (self._signifier, self.ratio, self._summary, self._signifier)
#      else:
#         return '{%s %s %s}' % (self._signifier, self.duration.multiplier, self._signifier)
#
#   ## PROPERTIES ##
#
#   @property
#   def duration(self):
#      '''Tuplet duration interface.'''
#      return self._duration

   pass
