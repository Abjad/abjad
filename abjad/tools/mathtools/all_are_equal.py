# -*- coding: utf-8 -*-


def all_are_equal(expr):
    '''Is true when `expr` is a sequence and all elements in `expr` are equal:

    ::

        >>> mathtools.all_are_equal([99, 99, 99, 99, 99, 99])
        True

    Is true when `expr` is an empty sequence:

    ::

        >>> mathtools.all_are_equal([])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_equal(17)
        False

    Returns true or false.
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
