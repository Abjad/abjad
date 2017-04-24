# -*- coding: utf-8 -*-


def all_are_pairs(argument):
    r'''Is true when `argument` is an iterable collection of pairs.
    Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.all_are_pairs([(1, 2), (3, 4), (5, 6), (7, 8)])
            True

        ::

            >>> mathtools.all_are_pairs('foo')
            False

    ..  container:: example

        Is true when `argument` is empty:

        ::

            >>> mathtools.all_are_pairs([])
            True

    Returns true or false.
    '''
    try:
        return all(len(_) == 2 for _ in argument)
    except TypeError:
        return False
