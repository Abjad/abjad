# -*- coding: utf-8 -*-


def all_are_pairs_of_types(expr, first_type, second_type):
    r'''Is true when `expr` is a sequence whose members are all sequences of
    length 2, and where the first member of each pair is an instance of
    `first_type` and where the second member of each pair is an instance
    of `second_type`.

    ::

        >>> mathtools.all_are_pairs_of_types([(1., 'a'), (2.1, 'b'), (3.45, 'c')], float, str)
        True

    Is true when `expr` is an empty sequence:

    ::

        >>> mathtools.all_are_pairs_of_types([], float, str)
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_pairs_of_types('foo', float, str)
        False

    Returns true or false.
    '''

    try:
        return all(len(x) == 2 and \
            isinstance(x[0], first_type) and \
            isinstance(x[1], second_type) for x in expr)
    except TypeError:
        return False
    except KeyError:
        return False
