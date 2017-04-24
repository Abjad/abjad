# -*- coding: utf-8 -*-


def is_integer_equivalent_pair(argument):
    r'''Is true when `argument` is a pair of integer-equivalent items.
    Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_integer_equivalent_pair((2.0, '3'))
            True

        ::

            >>> mathtools.is_integer_equivalent_pair((2.5, '3'))
            False

    Returns true or false.
    '''
    from abjad.tools import mathtools
    return (
        isinstance(argument, tuple) and
        len(argument) == 2 and
        all(mathtools.is_integer_equivalent(x) for x in argument)
        )
