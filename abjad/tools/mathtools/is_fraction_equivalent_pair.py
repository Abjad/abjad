# -*- coding: utf-8 -*-


def is_fraction_equivalent_pair(argument):
    r'''Is true when `argument` is an integer-equivalent pair of numbers
    excluding 0 as the second term. Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_fraction_equivalent_pair((2, 3))
            True

        ::

            >>> mathtools.is_fraction_equivalent_pair((2, 0))
            False

    Returns true or false.
    '''
    from abjad.tools import mathtools
    return (
        mathtools.is_integer_equivalent_pair(argument) and
        not argument[1] == 0
        )
