def are_relatively_prime(expr):
    '''.. versionadded:: 2.5

    True when `expr` is a sequence comprising zero or more numbers,
    all of which are relatively prime:

    ::

        >>> mathtools.are_relatively_prime([13, 14, 15])
        True

    Otherwise false:

    ::

        >>> mathtools.are_relatively_prime([13, 14, 15, 16])
        False

    Note that function returns true when `expr` is an empty sequence:

    ::

        >>> mathtools.are_relatively_prime([])
        True

    Function returns false when `expr` is nonsensical type:

    ::

        >>> mathtools.are_relatively_prime('foo')
        False

    Return boolean.
    '''
    from abjad.tools import mathtools

    try:
        all_factors = set([])
        for number in expr:
            current_factors = mathtools.factors(number)
            current_factors.remove(1)
            current_factors = set(current_factors)
            if all_factors & current_factors:
                return False
            all_factors.update(current_factors)
        return True
    # TODO: remove unqualified except
    except:
        return False
