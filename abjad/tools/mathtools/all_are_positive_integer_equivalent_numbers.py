# -*- coding: utf-8 -*-


def all_are_positive_integer_equivalent_numbers(argument):
    '''Is true when `argument` is an iterable collection of positive
    integer-equivalent numbers. Otherwise false.

    ..  container:: example

        ::

            >>> items = [Fraction(4, 2), 2.0, 2]
            >>> mathtools.all_are_positive_integer_equivalent_numbers(items)
            True

    Returns true or false.
    '''
    from abjad.tools import mathtools
    try:
        return all(
            mathtools.is_positive_integer_equivalent_number(_)
            for _ in argument
            )
    except TypeError:
        return False
