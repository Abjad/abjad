# -*- coding: utf-8 -*-


def all_are_unequal(argument):
    '''Is true when `argument` is an iterable collection of unequal items.
    Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.all_are_unequal([1, 2, 3, 4, 9])
            True

        ::

            >>> mathtools.all_are_unequal(17)
            False

    ..  container:: example

        Is true when `argument` is empty:

        ::

            >>> mathtools.all_are_unequal([])
            True

    Returns true or false.
    '''
    try:
        return argument == type(argument)(set(argument))
    except TypeError:
        return False
