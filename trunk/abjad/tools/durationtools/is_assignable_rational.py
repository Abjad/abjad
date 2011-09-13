from abjad.tools import mathtools
from fractions import Fraction


def is_assignable_rational(expr):
    r'''.. versionadded:: 1.1

    True when `expr` is assignable rational. Otherwise false::

        abjad> from abjad.tools import durationtools

    ::

        abjad> for numerator in range(0, 16 + 1):
        ...     duration = Fraction(numerator, 16)
        ...     print '%s\t%s' % (duration, durationtools.is_assignable_rational(duration))
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

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``durationtools.is_assignable()`` to
        ``durationtools.is_assignable_rational()``.
    '''

    try:
        duration = Fraction(expr)
    except (TypeError, ValueError):
        return False

    if isinstance(expr, float):
        return False

    if 0 < duration < 16:
        if mathtools.is_nonnegative_integer_power_of_two(duration.denominator):
            if mathtools.is_assignable_integer(duration.numerator):
                return True

    return False
