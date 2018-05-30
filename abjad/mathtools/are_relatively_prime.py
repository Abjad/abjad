import collections
import numbers


def are_relatively_prime(argument):
    """
    Is true when ``argument`` is an iterable collection of relative primes.

    ..  container:: example

        >>> abjad.mathtools.are_relatively_prime([13, 14, 15])
        True

        >>> abjad.mathtools.are_relatively_prime([13, 14, 15, 16])
        False

        >>> abjad.mathtools.are_relatively_prime('text')
        False

    ..  container:: example

        Returns true when ``argument`` is empty:

        >>> abjad.mathtools.are_relatively_prime([])
        True

    Returns true or false.
    """
    from abjad import mathtools
    if not isinstance(argument, collections.Iterable):
        return False
    if not all(isinstance(_, numbers.Number) for _ in argument):
        return False
    all_factors = set([])
    for number in argument:
        current_factors = mathtools.factors(number)
        current_factors = set(current_factors)
        if all_factors & current_factors:
            return False
        all_factors.update(current_factors)
    return True
