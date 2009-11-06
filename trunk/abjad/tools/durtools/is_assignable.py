from abjad.rational import Rational
from abjad.tools import mathtools


def is_assignable(duration):
   r'''True when rational-valued `duration` is 
   and of a form acceptable for assignment to written duration
   of a note, rest, chord or skip. Otherwise false.

   That is, `duration` must be rational of the form ``p/q``,
   such that:

   * ``0 < p/q 16``
   * ``q = 2**n`` with integer ``n``
   * ``p`` is a notehead-assignable integer.

   ::

      abjad> for numerator in range(0, 16 + 1):
      ...     duration = Rational(numerator, 16)
      ...     print '%s\t%s' % (duration, durtools.is_assignable(duration))
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
   '''

   duration = Rational(duration)
   return mathtools.is_power_of_two(duration._d) and \
      (0 < duration < 16) and \
      mathtools.is_assignable(duration._n)
