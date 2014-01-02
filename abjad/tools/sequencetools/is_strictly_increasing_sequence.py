# -*- encoding: utf-8 -*-


def is_strictly_increasing_sequence(expr):
    r'''Is true when `expr` is a sequence and the elements in `expr` increase strictly:

    ::

        >>> expr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> sequencetools.is_strictly_increasing_sequence(expr)
        True

    False when `expr` is a sequence and the elements in `expr` do not increase strictly:

    ::

        >>> expr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        >>> sequencetools.is_strictly_increasing_sequence(expr)
        False

    ::

        >>> expr = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
        >>> sequencetools.is_strictly_increasing_sequence(expr)
        False

    ::

        >>> expr = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        >>> sequencetools.is_strictly_increasing_sequence(expr)
        False

    ::

        >>> expr = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
        >>> sequencetools.is_strictly_increasing_sequence(expr)
        False

    Is true when `expr` is an empty sequence:

    ::

        >>> sequencetools.is_strictly_increasing_sequence([])
        True

    False when `expr` is not a sequence:

    ::

        >>> sequencetools.is_strictly_increasing_sequence(17)
        False

    Returns boolean.
    '''

    try:
        previous = None
        for current in expr:
            if previous is not None:
                if not previous < current:
                    return False
            previous = current
        return True
    except TypeError:
        return False
