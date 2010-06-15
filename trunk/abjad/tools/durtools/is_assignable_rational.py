from abjad.rational import Rational
from abjad.tools import mathtools


def is_assignable_rational(duration):
   r'''True when `duration` is of a form acceptable 
   for note-head assignment.

   That is, true when `duration` is a rational of the form ``p/q``,
   such that:

   * ``p`` is a notehead-assignable integer
   * ``q = 2**n`` with integer ``n``
   * ``0 < p/q 16``

   Otherwise false. ::

      abjad> for numerator in range(0, 16 + 1):
      ...     duration = Rational(numerator, 16)
      ...     print '%s\t%s' % (duration, durtools.is_assignable_rational(duration))
      ... 
      0     False
      1/16  True
      1/8   True
      3/16  True
      1/4   True
      5/16  False
      3/8   True
      7/16  True
      1/2   True
      9/16  False
      5/8   False
      11/16 False
      3/4   True
      13/16 False
      7/8   True
      15/16 True
      1     True

   .. versionchanged:: 1.1.2
      renamed ``durtools.is_assignable( )`` to
      ``durtools.is_assignable_rational( )``.

   .. versionchanged:: 1.1.2
      renamed ``durtools.is_assignable_duration( )`` to
      ``durtools.is_assignable_rational( )``.
   '''

   duration = Rational(duration)
   return mathtools.is_power_of_two(duration._d) and \
      (0 < duration < 16) and \
      mathtools.is_assignable_integer(duration._n)
