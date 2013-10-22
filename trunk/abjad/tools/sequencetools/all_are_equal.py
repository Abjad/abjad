# -*- encoding: utf-8 -*-


def all_are_equal(expr):
    '''True when `expr` is a sequence and all elements in `expr` are equal:

    ::

        >>> sequencetools.all_are_equal([99, 99, 99, 99, 99, 99])
        True

    True when `expr` is an empty sequence:

    ::

        >>> sequencetools.all_are_equal([])
        True

    False otherwise:

    ::

        >>> sequencetools.all_are_equal(17)
        False

    Returns boolean.
    '''

    try:
        first_element = None
        for element in expr:
            if first_element is None:
                first_element = element
            else:
                if not element == first_element:
                    return False
        return True
    except TypeError:
        return False
