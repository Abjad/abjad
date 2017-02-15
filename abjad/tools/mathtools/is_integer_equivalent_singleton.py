# -*- coding: utf-8 -*-


def is_integer_equivalent_singleton(argument):
    r'''Is true when `argument` is a singleton of integer-equivalent items.
    Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_integer_equivalent_singleton((2.0,))
            True

        ::

            >>> mathtools.is_integer_equivalent_singleton((2.5,))
            False

    Returns true or false.
    '''
    from abjad.tools import mathtools
    return (
        isinstance(argument, tuple) and
        len(argument) == 1 and
        all(mathtools.is_integer_equivalent(_) for _ in argument)
        )
