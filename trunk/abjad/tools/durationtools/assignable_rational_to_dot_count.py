from abjad.tools import mathtools
from abjad.tools.durationtools.is_assignable_rational import is_assignable_rational


def assignable_rational_to_dot_count(rational):
    r'''.. versionadded:: 2.0

    Change assignable `rational` to dot count::

        abjad> from abjad.tools import durationtools

    ::

        abjad> for n in range(1, 9):
        ...     try:
        ...                 rational = Fraction(n, 16)
        ...                 dot_count = durationtools.assignable_rational_to_dot_count(rational)
        ...                 print '%s\t%s' % (rational, dot_count)
        ...     except AssignabilityError:
        ...                 pass
        ...
        1/16    0
        1/8     0
        3/16    1
        1/4     0
        3/8     1
        7/16    2
        1/2     0

    Raise assignability error when `rational` not assignable.

    Return nonnegative integer.
    '''

    if not is_assignable_rational(rational):
        raise AssignabilityError

    binary_string = mathtools.integer_to_binary_string(rational.numerator)
    digit_sum = sum([int(x) for x in list(binary_string)])
    dot_count = digit_sum - 1

    return dot_count
