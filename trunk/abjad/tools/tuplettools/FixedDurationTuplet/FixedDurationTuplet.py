from abjad.core import Fraction
from abjad.tools.tuplettools.FixedDurationTuplet._FixedDurationTupletDurationInterface \
   import _FixedDurationTupletDurationInterface
from abjad.components.Tuplet.Tuplet import Tuplet


class FixedDurationTuplet(Tuplet):

   def __init__(self, duration, music, **kwargs):
      ## new ##
      dummy_multiplier = 1
      Tuplet.__init__(self, dummy_multiplier, music)
      ## end ##
      self._duration = _FixedDurationTupletDurationInterface(self, duration)
      self._signifier = '@'
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##
 
   def __repr__(self):
      return '%s(%s, [%s])' % (
         self.__class__.__name__, self.duration.target, self._summary)

   def __str__(self):
      if 0 < len(self):
         return '{%s %s %s %s}' % (self._signifier, self.ratio, self._summary, self._signifier)
      else:
         return '{%s %s %s}' % (self._signifier, self.duration.target, self._signifier)

   ## PUBLIC METHODS ##

   def trim(self, start, stop = 'unused'):
      if stop != 'unused':
         assert not (start == 0 and (stop is None or len(self) <= stop))
      old_multiplier = self.duration.multiplier
      if stop == 'unused':
         del(self[start])
      else:
         del(self[start:stop])
      self.duration.target = old_multiplier * self.duration.contents
