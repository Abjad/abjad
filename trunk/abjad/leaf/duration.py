from abjad.component.duration import _ComponentDurationInterface
from abjad.core.interface import _Interface
from abjad.exceptions.exceptions import AssignabilityError
from abjad.helpers.binary_string import binary_string
from abjad.helpers.is_assignable import is_assignable
from abjad.rational.rational import Rational
from abjad.tools import duration
import math


class _LeafDurationInterface(_ComponentDurationInterface):

   def __init__(self, _client, duration_token):
      _ComponentDurationInterface.__init__(self, _client)
      self.multiplier = None
      self.written = Rational(*duration.token_unpack(duration_token))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _dots(self):
      return sum([int(x) for x in list(binary_string(self.written._n))]) - 1

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
         if not is_assignable(rational):
            raise AssignabilityError('%s' % str(rational))
         self._written = rational
      return property(**locals( ))
