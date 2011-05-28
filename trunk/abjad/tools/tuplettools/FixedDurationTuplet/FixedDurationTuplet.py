from fractions import Fraction
from abjad.tools.tuplettools.FixedDurationTuplet._FixedDurationTupletDurationInterface import _FixedDurationTupletDurationInterface
from abjad.components.Tuplet.Tuplet import Tuplet


class FixedDurationTuplet(Tuplet):
   '''Abjad tuplet of fixed duration and variable multiplier:

   ::

      abjad> tuplettools.FixedDurationTuplet(Fraction(2, 8), "c'8 d'8 e'8")
      FixedDurationTuplet(1/4, [c'8, d'8, e'8])
   '''

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
      '''Trim fixed-duration tuplet elements from `start` to `stop`::

         abjad> tuplet = tuplettools.FixedDurationTuplet(Fraction(2, 8), "c'8 d'8 e'8")
         abjad> tuplet
         FixedDurationTuplet(1/4, [c'8, d'8, e'8])

      ::

         abjad> tuplet.trim(2)
         abjad> tuplet
         FixedDurationTuplet(1/6, [c'8, d'8])

      Preserve fixed-duration tuplet multiplier.

      Adjust fixed-duration tuplet duration.

      Return none.
      '''
      if stop != 'unused':
         assert not (start == 0 and (stop is None or len(self) <= stop))
      old_multiplier = self.duration.multiplier
      if stop == 'unused':
         del(self[start])
      else:
         del(self[start:stop])
      self.duration.target = old_multiplier * self.duration.contents
