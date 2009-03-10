from abjad.core.duration import _DurationInterface
from abjad.core.interface import _Interface
from abjad.exceptions.exceptions import AssignabilityError
from abjad.helpers.binary import _binary
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.hasname import hasname
from abjad.helpers.is_assignable import _is_assignable
from abjad.rational.rational import Rational
import math


class _LeafDurationInterface(_DurationInterface):

   def __init__(self, _client, duration):
      _DurationInterface.__init__(self, _client)
      self.multiplier = None
      self.written = Rational(*_duration_token_unpack(duration))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _dots(self):
      return sum([int(x) for x in list(_binary(self.written._n))]) - 1

   @property
   def _dotted(self):
      durationNames = {0.5:r'\breve', 0.25:r'\longa', 0.125:r'\maxima'}
      number = self._number
      if number in durationNames:
         number = durationNames[number]
      return '%s%s' % (number, '.' * self._dots)

   @property
   def _duration(self):
      if self.multiplier is not None:
         return self.written * self.multiplier
      else:
         return self.written

   @property
   def _flags(self):
      return max(-int(math.floor(math.log(float(self.written._n) / \
         self.written._d, 2))) - 2, 0)

   @property
   def _number(self):
      return 2 ** int(math.ceil(math.log(1/self.written, 2)))

   @property
   def _product(self):
      if self.multiplier is not None:
         return '%s * %s' % (self._dotted, self.multiplier)
      else:
         return self._dotted

   ## PUBLIC ATTRIBUTES ##

   @property
   def multiplied(self):
      if self.written:
         if self.multiplier:
            return self.written * self.multiplier
         else:
            return Rational(self.written)
      else:
         return None

   @apply
   def multiplier( ):
      def fget(self):
         return self._multiplier
      def fset(self, expr):
         if expr is None:
            self._multiplier = None
         else:
            if isinstance(expr, Rational):
               rational = expr
            elif isinstance(expr, (int, long)):
               rational = Rational(expr)
            else:
               raise ValueError('can not set duration multiplier')
            assert rational >= 0
            self._multiplier = rational
      return property(**locals( ))

   @apply
   def preprolated( ):
      def fget(self):
         return self.multiplied
      return property(**locals( ))

   @apply
   def written( ):
      def fget(self):
         return self._written
      def fset(self, expr):
         if isinstance(expr, Rational):
            rational = expr
         elif isinstance(expr, (int, long)):
            rational = Rational(expr)
         else:
            raise ValueError('can not set written duration.')
         if not _is_assignable(rational):
            raise AssignabilityError('%s' % str(rational))
         self._written = rational
      return property(**locals( ))

   ## PUBLIC METHODS ##

   ## TODO: Externalize to leaf_duration_rewrite(leaf) helper
   
   def rewrite(self, target):
      previous = self.multiplied
      self.written = Rational(*_duration_token_unpack(target))
      self.multiplier = None
      multiplier = previous / self.written
      if multiplier != 1:
         self.multiplier = multiplier
