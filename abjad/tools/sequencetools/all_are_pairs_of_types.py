# -*- encoding: utf-8 -*-


def all_are_pairs_of_types(expr, first_type, second_type):
    r'''True when `expr` is a sequence whose members are all sequences of length 2,
    and where the first member of each pair is an instance of `first_type` and
    where the second member of each pair is an instance of `second_type`:

    ::

        >>> sequencetools.all_are_pairs_of_types([(1., 'a'), (2.1, 'b'), (3.45, 'c')], float, str)
        True

    True when `expr` is an empty sequence:

    ::

        >>> sequencetools.all_are_pairs_of_types([], float, str)
        True

    Otherwise false:

    ::

        >>> sequencetools.all_are_pairs_of_types('foo', float, str)
        False

    Returns boolean.
    '''

    try:
        return all(len(x) == 2 and \
            isinstance(x[0], first_type) and \
            isinstance(x[1], second_type) for x in expr)
    except TypeError:
        return False
    except KeyError:
        return False
